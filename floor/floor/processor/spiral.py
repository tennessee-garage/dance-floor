from builtins import range
import collections
import colorsys

from floor.processor.base import Base
from floor.processor.utils import clocked
from floor.processor.constants import COLOR_MAXIMUM

#  0  1  2  3  4  5  6  7
#  8  9 10 11 12 13 14 15
# 16 17 18 19 20 21 22 23
# 24 25 26 27 28 29 30 31
# 32 33 34 35 36 37 38 39
# 40 41 42 43 44 45 46 47
# 48 49 50 51 52 53 54 55
# 56 57 58 59 60 61 62 63

READ_ORDER = [27, 28,
              36, 35, 34,
              26, 18,
              19, 20, 21,
              29, 37, 45,
              44, 43, 42, 41,
              33, 25, 17, 9,
              10, 11, 12, 13, 14,
              22, 30, 38, 46, 54,
              53, 52, 51, 50, 49, 48,
              40, 32, 24, 16,  8,  0,
               1,  2,  3,  4,  5,  6,  7,
              15, 23, 31, 39, 47, 55, 63,
              62, 61, 60, 59, 58, 57, 56]

TRIAD = [0.0, 0.5 + (1.0/12.0), 0.5 - (1.0/12.0)]


class Spiral(Base):
    """Spiral out from the center."""

    def __init__(self, **kwargs):
        super(Spiral, self).__init__(**kwargs)

        palette = kwargs.get("palette", 1)

        self.t = 0.0
        self.delta = 0.1

        self.hue = 0.0
        self.sat = 1.0
        self.val = 1.0

        if palette == 0:
            # How much to move hue forward
            self.hue_drift = 0.001
            # By how much to jump hue on every X steps
            self.jumps = [TRIAD[0], TRIAD[0], TRIAD[0], TRIAD[1],
                          TRIAD[0], TRIAD[0], TRIAD[0], TRIAD[2]]
        elif palette == 1:
            self.hue_drift = 0.001
            self.jumps = [TRIAD[0] for _ in range(32)] +\
                         [TRIAD[1] for _ in range(8)] +\
                         [TRIAD[0] for _ in range(32)] +\
                         [TRIAD[2] for _ in range(8)]
        elif palette == 2:
            self.hue_drift = 0.001
            self.jumps = [TRIAD[i] for _ in range(16) for i in range(2)] +\
                         [TRIAD[2] for _ in range(4)]
        elif palette == 3:
            self.hue_drift = 0.005
            self.jumps = [TRIAD[0]]

        # A counter for what part of the jump we're in
        self.count = 0
        # How often count should repeat
        self.count_mod = len(self.jumps)

        self.pixels = [[0 for _ in range(3)] for _ in range(64)]
        self.train = collections.deque([[0 for _ in range(3)] for _ in range(64)])

    @clocked(frames_per_second=24)
    def get_next_frame(self, context):
        self.hue += self.hue_drift
        # Wrap around if we hit 1.0
        if self.hue > 1.0:
            self.hue -= 1.0

        jump_hue = self.hue + self.jumps[self.count]
        if jump_hue > 1.0:
            jump_hue -= 1.0

        self.count = (self.count + 1) % self.count_mod

        r, g, b = colorsys.hsv_to_rgb(jump_hue, self.sat, self.val)
        pixel = [r * COLOR_MAXIMUM, g * COLOR_MAXIMUM, b * COLOR_MAXIMUM]

        self.train.pop()
        self.train.appendleft(pixel)

        for idx in range(64):
            self.pixels[READ_ORDER[idx]] = self.train[idx]

        self.t += self.delta

        return self.pixels
