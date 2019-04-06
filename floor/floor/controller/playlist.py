from builtins import object
import json
from time import time
import logging

logger = logging.getLogger('playlist')


class PlaylistError(Exception):
    """Top-level error for Playlist class."""


class ProcessorNotFound(PlaylistError):
    """Thrown when attempting to append an unknown processor."""


class Playlist(object):
    def __init__(self, all_processors):
        self.all_processors = all_processors
        # The index into the queue array
        self.position = None
        # Time when the playlist should auto advance.
        self.next_advance = None
        self.queue = []
        self.running = True

    @classmethod
    def from_file(cls, all_processors, filename, strict=False):
        playlist = cls(all_processors)
        playlist.load_from(filename, strict=strict)
        return playlist

    @classmethod
    def from_single_processor(cls, processor):
        all_processors = [processor]
        playlist = cls(all_processors)
        playlist.append(processor.__class__.__name__)
        return playlist

    @staticmethod
    def item(name, duration=0, args=None):
        """Builds a playlist entry."""
        return {
            'name': name,
            'duration': int(duration),
            'args': args,
        }

    def __len__(self):
        return len(self.queue)

    def clear(self):
        self.position = None
        self.next_advance = None
        self.queue = []

    def load_from(self, input_filename, strict=False):
        """Replaces the current playlist with contents of the file."""
        self.clear()
        with open(input_filename) as json_data:
            items = json.load(json_data).get('queue', [])
            for item in items:
                name = item['name']
                try:
                    duration = int(item.get('duration', 0))
                except ValueError:
                    duration = 0
                args = item.get('args')
                try:
                    self.append(name, duration, args)
                except ProcessorNotFound as e:
                    if strict:
                        raise e
                    else:
                        logger.warning(e)

    def save_to(self, output_filename):
        playlist = {
            "queue": self.queue,
        }
        with open(output_filename, 'w') as fp:
            fp.write(json.dumps(playlist, indent=2))
            fp.write('\n')

    def is_running(self):
        return self.running

    def stop_playlist(self):
        current = self.queue[self.position]

        # Save time remaining
        if self.next_advance is not None:
            current['remaining_duration'] = self.next_advance - time()
        else:
            current['remaining_duration'] = None
        self.next_advance = None

        self.running = False

    def start_playlist(self):
        current = self.queue[self.position]

        if current['remaining_duration'] is not None:
            # Restore time remaining
            self.next_advance = time() + current['remaining_duration']
        else:
            self.next_advance = None

        self.running = True

    def append(self, name, duration=0, args=None):
        """Add an item at the end of the playlist."""
        if name not in self.all_processors:
            raise ProcessorNotFound('Processor "{}" is unknown'.format(name))
        self.queue.append(Playlist.item(name, duration, args))
        return len(self.queue) - 1

    def insert_next(self, name, duration=0, args=None):
        """Add an item at the current position in the playlist."""
        if name not in self.all_processors:
            raise ProcessorNotFound('Processor "{}" is unknown'.format(name))
        position = self.position
        position = max(0, position)  # handle position=-1
        self.queue.insert(self.position, Playlist.item(name, duration, args))
        return position

    def get_current(self):
        """Get the current item, advancing if it's time to."""
        if not self.queue:
            return None

        if self.position is None:
            # First call: Start the first item.
            self.advance()
        elif self.next_advance is not None and (time() > self.next_advance):
            self.advance()

        return self.queue[self.position]

    def advance(self):
        """Go to the next playlist item."""
        if self.position is None:
            position = 0
        else:
            position = (self.position + 1) % len(self.queue)
        self.go_to(position)

    def previous(self):
        """Go to the previous playlist item."""
        if self.position is None:
            position = 0
        else:
            position = (self.position - 1) % len(self.queue)
        self.go_to(position)

    def go_to(self, position):
        """Go to a specific playlist item."""
        if not self.is_running():
            return

        queue_length = len(self.queue)
        if position >= queue_length:
            raise ValueError('Position {} out of range ({})'.format(position, queue_length))
        self.position = position

        current = self.queue[self.position]
        if current['duration']:
            self.next_advance = time() + current['duration']
        else:
            self.next_advance = None

        logger.info('Advanced to: {} (position={})'.format(current['name'], self.position))

    def remove(self, position):
        """Removes an item from the playlist. If removing the current item,
        advances to the next item as a side-effect.
        """
        if position >= len(self.queue) or position < 0:
            raise ValueError('Position {} out of range ({})'.format(position, len(self.queue)))
        if len(self.queue) == 1:
            raise ValueError('Cannot delete the last item in playlist.')

        del self.queue[position]
        if position < self.position:
            # Position was behind current.
            self.position -= 1
        elif position == self.position:
            # Removed current.
            self.position -= 1
            self.advance()
        else:
            # Position was ahead of current.
            pass

    def stay(self):
        self.next_advance = None
