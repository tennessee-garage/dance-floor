from builtins import object
import json


class Layout(object):
    def __init__(self, config_filename):
        self.squares = None
        self.rows = None
        self.cols = None
        self.layout = None

        with open(config_filename) as json_data:
            config = json.load(json_data)

            # NOTE: The only thing currently used from config is the layout definition to
            # and then only to mark certain tiles as dead/bypassed.  If a square position
            # is a 1 that means the square is active.  If its 0 then the square has been bypassed
            # with a cable, so we need to skip writing that squares data so that things don't
            # get out of sync
            self.squares = config.get('squares', 64)
            self.rows = config.get('rows', 8)
            self.cols = config.get('cols', 8)
            self.layout = config.get('layout', None)

    def is_bypassed(self, num):
        return self.layout[num] == 0
