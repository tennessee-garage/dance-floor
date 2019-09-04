from builtins import object
import json
import os


class Layout(object):
    DEFAULT_CONFIG_NAME = 'floor-layout'

    def __init__(self, config_dir, config_name=None):
        self.config_dir = config_dir
        self.squares = None
        self.rows = None
        self.cols = None
        self.layout = None

        if not config_name:
            config_name = self.DEFAULT_CONFIG_NAME

        self.load_config_from_name(config_name)

    def load_config_from_name(self, name):
        config_path = os.path.join(self.config_dir, name + '.json')
        self.load_config_from_path(config_path)

    def load_config_from_path(self, path):
        with open(path) as json_data:
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
