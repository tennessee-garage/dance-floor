import colorsys
import math
import random
from builtins import object, range

from floor.processor.base import Base
from floor.processor.constants import COLOR_MAXIMUM
from floor.processor.utils import clocked


class Fire(Base):
    """Spiral out from the center."""

    def __init__(self, **kwargs):
        super(Fire, self).__init__(**kwargs)

        self.count = 0.0
        self.count_delta = 0.1
        self.spawn_chance = 0.3

        self.max_in_flight = 40
        self.in_flight = []

    def can_spawn_ember(self):
        """Max self.spawn_chance chance of spawning a ball, modulated by a sine curve."""
        val = random.random() * (math.sin(self.count) + 1.0)
        return val > self.spawn_chance

    @clocked(frames_per_second=24)
    def get_next_frame(self, context):
        pixels = [[0 for _ in range(3)] for _ in range(64)]

        if len(self.in_flight) < self.max_in_flight:
            if self.can_spawn_ember():
                ball = Ember()
                self.in_flight.append(ball)

        remaining = []
        for ember in self.in_flight:
            row_pos = int(round(ember.position))
            if row_pos <= 7:
                index = int(round(ember.position)) + (ember.row * 8)
                r, g, b = colorsys.hsv_to_rgb(ember.hue, 1.0, 1.0)
                pixels[index] = [
                    int(r * COLOR_MAXIMUM),
                    int(g * COLOR_MAXIMUM),
                    int(b * COLOR_MAXIMUM),
                ]

            ember.run()

            if not ember.finished:
                remaining.append(ember)

        self.in_flight = remaining
        self.count += self.count_delta

        return pixels


class Ember(object):
    SLOW_HUE = 0.0  # red
    FAST_HUE = 0.2  # yellow

    MAX_SPEED = 18.0

    def __init__(self):
        self.t = 0
        self.delta = 0.04

        self.hue = self.SLOW_HUE
        self.row = random.randrange(8)
        self.speed = random.random() * self.MAX_SPEED
        self.position = 0

        self.finished = False

    def run(self):
        self.position = (self.speed * self.t) + (-9.8 * self.t**2)
        col_range = (self.speed + (-9.8 * self.t)) / self.MAX_SPEED

        if col_range > 1.0:
            col_range = 1.0

        self.hue = (col_range * (self.FAST_HUE - self.SLOW_HUE)) + self.SLOW_HUE

        if self.position < 0.0:
            self.finished = True
            return

        if self.position > 7.5:
            self.finished = True
            return

        self.t += self.delta
