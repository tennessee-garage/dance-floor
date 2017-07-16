import json
from time import time
import sys


class Playlist(object):

    def __init__(self, config_dir='', processor=None):
        # The index into the queue array
        self.position = -1
        # When the current processor started
        self.start_time = None
        # The current processor entry
        self.current = None
        # The current duration
        self.current_duration = None

        self.queue = []

        # If a processor was passed in, use it, otherwise read the config file
        if processor:
            self.append(name=processor)
        else:
            filename = config_dir + "/playlist-default.json"
            with open(filename) as json_data:
                items = json.load(json_data).get('queue', [])
                for item in items:
                    self.append(
                        item['name'],
                        item.get('duration', 0),
                        item.get('args')
                    )

    @staticmethod
    def item(name, duration=0, args=None):
        """Builds a playlist entry."""
        return {
            'name': name,
            'duration': int(duration),
            'args': args,
        }

    def append(self, name, duration=0, args=None):
        """Add an item at the end of the playlist."""
        self.queue.append(Playlist.item(name, duration, args))
        return len(self.queue) - 1

    def insert_next(self, name, duration=0, args=None):
        """Add an item at the current position in the playlist."""
        position = self.position
        position = max(0, position)  # handle position=-1
        self.queue.insert(self.position, Playlist.item(name, duration, args))
        return position

    def next_ready(self):
        # If we just started, we're ready for a new processor
        if self.position == -1:
            return True

        # A duration of zero means "forever".  If non-zero, check our run time
        if self.current_duration > 0:
            if (time() - self.start_time) > self.current_duration:
                return True

        return False

    def advance(self):
        """Go to the next playlist item."""
        position = (self.position + 1) % len(self.queue)
        self.go_to(position)

    def go_to(self, position):
        """Go to a specific playlist item."""
        queue_length = len(self.queue)
        if position >= queue_length:
            raise ValueError('Position {} out of range ({})'.format(position, queue_length))
        self.position = position
        self.current = self.queue[position]
        self.current_duration = self.current["duration"]
        self.start_time = time()

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

    def get_processor_name(self):
        if not self.current:
            return None
        return self.current["name"]

    def get_processor_args(self):
        if not self.current:
            return None
        if "args" in self.current:
            return self.current["args"]
        else:
            return None
