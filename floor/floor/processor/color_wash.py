from builtins import range
from floor.processor.base import Base
from floor.processor.utils import clocked
from floor.processor.constants import COLOR_MAXIMUM


class ColorWash(Base):
    def __init__(self, **kwargs):
        super(ColorWash, self).__init__(**kwargs)
        self.red = 0
        self.green = 0
        self.blue = 0

    @clocked(frames_per_second=24)
    def get_next_frame(self, context):
        pixels = []

        for x in range(0, 8):
            for y in range(0, 8):
                pixels.append((
                    (self.red * x) % COLOR_MAXIMUM,
                    (self.green * y) % COLOR_MAXIMUM,
                    self.blue % COLOR_MAXIMUM
                ))

        self.red += 1
        self.green += 1
        self.blue += 1

        return pixels
