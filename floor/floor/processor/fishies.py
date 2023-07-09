import random
import time
from builtins import range

import floor.util.color_utils as color
from floor.processor.base import Base
from floor.processor.utils import clocked


class Fishies(Base):
    def __init__(self, **kwargs):
        super(Fishies, self).__init__(**kwargs)
        self.pixels = []
        self.palette = color.get_palette("rainbow_bunny")
        self.palette_length = len(self.palette)
        self.fishies = self.init_fishies()
        self.last_time = None
        for x in range(0, 8):
            for y in range(0, 8):
                self.pixels.append((0, 0, 0))

    def rand_color(self):
        idx = random.randint(0, self.palette_length - 1)
        return self.palette[idx]

    def init_fishies(self):
        fishies = []
        fishies.append({"x": 0, "y": 0, "dx": 1, "dy": 1, "c": self.palette[0]})
        fishies.append({"x": 0, "y": 7, "dx": -1, "dy": -1, "c": self.palette[1]})
        fishies.append({"x": 7, "y": 0, "dx": -1, "dy": 1, "c": self.palette[3]})
        fishies.append({"x": 7, "y": 7, "dx": -1, "dy": -1, "c": self.palette[4]})
        # fishies.append({'x':3, 'y':3, 'dx':-1, 'dy':-1, 'c':self.palette[4]})
        return fishies

    def swim(self, fish):
        # swim in a random direction
        chance = random.random()
        if chance > 0.9:
            fish["dx"] = random.randint(-1, 1)
        fish["x"] += fish["dx"]
        if fish["x"] < 0:
            fish["x"] = 0
            fish["dx"] = -1 * fish["dx"]
        if fish["x"] > 7:
            fish["x"] = 7
            fish["dx"] = -1 * fish["dx"]

        chance = random.random()
        if chance > 0.9:
            fish["dy"] = random.randint(-1, 1)
        fish["y"] += fish["dy"]
        if fish["y"] < 0:
            fish["y"] = 0
            fish["dy"] = -1 * fish["dy"]
        if fish["y"] > 7:
            fish["y"] = 7
            fish["dy"] = -1 * fish["dy"]

    @clocked(frames_per_second=24)
    def get_next_frame(self, context):
        if self.last_time is None:
            self.last_time = context.clock
        next_time = context.clock
        d_time = next_time - self.last_time

        for index in range(len(self.fishies)):
            fish = self.fishies[index]
            chance = random.random()
            if d_time > 0.2:
                self.swim(fish)
                self.last_time = next_time
            self.pixels[fish["y"] * 8 + fish["x"]] = fish["c"]

        for index in range(len(self.pixels)):
            px = self.pixels[index]
            px = color.scale_color(px, 0.7)
            self.pixels[index] = px

        return self.pixels
