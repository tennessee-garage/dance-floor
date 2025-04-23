from __future__ import print_function

import colorsys
import math
from builtins import range

from floor.processor.base import Base
from floor.processor.constants import COLOR_MAXIMUM
from floor.processor.utils import clocked
from floor.util.easing import Easing


class LineSlam(Base):
    """Spiral out from the center."""

    def __init__(self, **kwargs):
        super(LineSlam, self).__init__(**kwargs)
        self.t_start = None
        self.t_end = None
        self.end_pause = 1.0

        self.stage = 1
        self.easing1 = Easing(duration=0.5, start=0.0, end=7.0)
        self.easing2 = Easing(duration=0.5, start=0.0, end=1.0)

    @clocked(frames_per_second=120)
    def get_next_frame(self, context):
        if self.stage == 1:
            pixels = self.stage_1()
        elif self.stage == 2:
            pixels = self.stage_2()
        else:
            print("-- reset")
            self.reset_stage()
            pixels = self.PIXELS_ALL_OFF

        return pixels

    def stage_1(self):
        """
        Stage one - line slams down
        :return: list - pixels
        """
        self.easing1.mark()
        if self.easing1.is_finished():
            self.stage += 1

        pixels = []

        cur = self.easing1.ease_in_circ()

        pre = 1.0 - (cur - int(cur))
        post = 1.0 - (int(cur + 1.0) - cur)

        for y in range(8):
            for x in range(8):
                if y == int(cur):
                    pixels.append((int(COLOR_MAXIMUM * pre), 0, 0))
                elif y == int(cur + 1):
                    pixels.append((int(COLOR_MAXIMUM * post), 0, 0))
                else:
                    pixels.append((0, 0, 0))

        return pixels

    def stage_2(self):
        self.easing2.mark()
        if self.easing2.is_finished():
            self.stage += 1

        pixels = []

        cur = self.easing2.ease_in_circ()

        for y in range(8):
            for x in range(8):
                if y == 7:
                    r, g, b = colorsys.hsv_to_rgb(0.0, cur, 1.0 - cur)
                    pixels.append((COLOR_MAXIMUM * r, COLOR_MAXIMUM * g, COLOR_MAXIMUM * b))
                else:
                    pixels.append((0, 0, 0))

        return pixels

    def reset_stage(self):
        self.easing1.reset()
        self.easing2.reset()
        self.stage = 1
