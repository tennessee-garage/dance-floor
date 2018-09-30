import time
import math

from base import Base
from floor.util import color_utils


class RaverPlaid(Base):

    def __init__(self, **kwargs):
        super(RaverPlaid, self).__init__(**kwargs)

        self.n_pixels = 64

        # how many sine wave cycles are squeezed into our n_pixels
        # 24 happens to create nice diagonal stripes on the wall layout
        self.freq_r = 24
        self.freq_g = 24
        self.freq_b = 24

        # how many seconds the color sine waves take to shift through a complete cycle
        self.speed_r = 7
        self.speed_g = -13
        self.speed_b = 19

        self.start_time = time.time()

    def get_next_frame(self, weights):
        t = (time.time() - self.start_time) * 5
        pixels = []
        for ii in range(self.n_pixels):
            pct = 1.0 * ii / self.n_pixels

            # diagonal black stripes
            pct_jittered = (pct * 77) % 37
            blackstripes = color_utils.cos(pct_jittered, offset=t * 0.05, period=1, minn=-1.5, maxx=1.5)
            blackstripes_offset = color_utils.cos(t, offset=0.9, period=60, minn=-0.5, maxx=3)
            blackstripes = color_utils.clamp(blackstripes + blackstripes_offset, 0, 1)

            # 3 sine waves for r, g, b which are out of sync with each other
            r = blackstripes * color_utils.remap(
                math.cos((t / self.speed_r + pct * self.freq_r) * math.pi * 2), -1, 1, 0, self.max_value)

            g = blackstripes * color_utils.remap(
                math.cos((t / self.speed_g + pct * self.freq_g) * math.pi * 2), -1, 1, 0, self.max_value)

            b = blackstripes * color_utils.remap(
                math.cos((t / self.speed_b + pct * self.freq_b) * math.pi * 2), -1, 1, 0, self.max_value)

            pixels.append((r, g, b))

        return pixels
