import json
from time import time
import sys


class Playlist(object):

    def __init__(self, config_dir='', processor=None):
        self.file = config_dir + "/playlist-default.json"

        # The index into the queue array
        self.position = -1
        # When the current processor started
        self.start_time = None
        # The current processor entry
        self.current = None
        # The current duration
        self.current_duration = None

        # If a processor was passed in, use it, otherwise read the config file
        if processor:
            self.data = {
                "queue": [
                    {
                        "name": processor,
                        "duration": "0",
                    }
                ]
            }
        else:
            with open(self.file) as json_data:
                self.data = json.load(json_data)

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
        queue = self.data["queue"]
        queue_length = len(queue)
        self.position = (self.position + 1) % queue_length
        self.current = queue[self.position]
        self.current_duration = int(self.current["duration"])
        self.start_time = time()

    def get_processor_name(self):
        return self.current["name"]

    def get_processor_args(self):
        if "args" in self.current:
            return self.current["args"]
        else:
            return None
