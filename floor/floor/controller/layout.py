import glob
import json
import os
import re
from builtins import object


class Layout(object):
    LAYOUT_MAPPING_DIR = "layouts"
    DEFAULT_CONFIG_NAME = "floor-layout"

    def __init__(self, config_dir, config_name=None):
        self.layout_dir = os.path.join(config_dir, self.LAYOUT_MAPPING_DIR)
        self.squares = None
        self.rows = None
        self.cols = None
        self.layout = None

        if not config_name:
            config_name = self.DEFAULT_CONFIG_NAME

        self.name = config_name
        self.load_config_from_name(config_name)

    @classmethod
    def from_squares(cls, config_dir, num_squares):
        layouts = cls.get_layout_mappings(config_dir)
        config_name = cls.DEFAULT_CONFIG_NAME

        # Pick the first layout that has at least as many squares as we've probed
        for layout in sorted(layouts, key=lambda a: a["num"]):
            if num_squares > layout["num"]:
                continue
            config_name = layout["name"]
            break

        return Layout(config_dir, config_name)

    @classmethod
    def get_layout_mappings(cls, config_dir):
        layout_dir = os.path.join(config_dir, cls.LAYOUT_MAPPING_DIR)
        layouts = []

        for filename in glob.glob(os.path.join(layout_dir, "*.json")):
            result = re.search(r"([^/]+)\.json$", filename)
            if not result:
                continue
            config_name = result.group(1)

            with open(filename) as json_data:
                config = json.load(json_data)
                layouts.append({"name": config_name, "num": config.get("squares")})

        return layouts

    def load_config_from_name(self, name):
        config_path = os.path.join(self.layout_dir, name + ".json")
        self.load_config_from_path(config_path)

    def load_config_from_path(self, path):
        with open(path) as json_data:
            config = json.load(json_data)

            # NOTE: The only thing currently used from config is the layout definition to
            # and then only to mark certain tiles as dead/bypassed.  If a square position
            # is a 1 that means the square is active.  If its 0 then the square has been bypassed
            # with a cable, so we need to skip writing that squares data so that things don't
            # get out of sync
            self.squares = config.get("squares", 64)
            self.rows = config.get("rows", 8)
            self.cols = config.get("cols", 8)
            self.layout = config.get("layout", None)

    def is_bypassed(self, num):
        return self.layout[num] == 0
