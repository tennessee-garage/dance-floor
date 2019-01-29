import random

from floor.processor.base import Base
from floor.processor.utils import clocked
from floor.processor.constants import COLOR_MAXIMUM


class RandomDecay(Base):
    def __init__(self, **kwargs):
        super(RandomDecay, self).__init__(**kwargs)
        self.red = 0
        self.green = 0
        self.blue = 0
        self.pixels = []

        for x in range(0, 8):
            for y in range(0, 8):
                self.pixels.append((
                    COLOR_MAXIMUM * random.random(),
                    COLOR_MAXIMUM * random.random(),
                    COLOR_MAXIMUM * random.random()
                ))

    @clocked(frames_per_second=24)
    def get_next_frame(self, context):
        next_pixels = []
        decay_rate = 0.9

        for x in range(0, 8):
            for y in range(0, 8):
                next_pixel = self.pixels[x*8 + y]
                next_red = decay_rate*next_pixel[0]
                next_blue = decay_rate*next_pixel[1]
                next_green = decay_rate*next_pixel[2]
                if (next_red + next_blue + next_green) < 10:
                    next_red = COLOR_MAXIMUM * random.random()
                    next_blue = COLOR_MAXIMUM * random.random()
                    next_green = COLOR_MAXIMUM * random.random()
                next_pixels.append((
                    next_red,
                    next_blue,
                    next_green
                ))

        self.pixels = next_pixels

        return self.pixels
