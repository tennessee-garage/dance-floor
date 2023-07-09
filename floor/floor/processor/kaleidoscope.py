import random
from builtins import range

import floor.util.color_utils as color
from floor.processor.base import Base
from floor.processor.utils import clocked


class Kaleidoscope(Base):
    LIFETIME = 1.0

    def __init__(self, **kwargs):
        super(Kaleidoscope, self).__init__(**kwargs)
        self.active_px = []
        self.times = [0 for _ in range(64)]
        self.palette = color.get_random_palette()
        self.palette_length = len(self.palette)

        for x in range(0, 64):
            self.active_px.append((0, 0, 0))
            self.times.append(0)

    def handle_weight_input(self, context):
        # Weight values are either 0 or 1.  If 1 consider it a step and add a pixel
        for i in range(0, 64):
            if context.weights[i] > 0 and self.times[i] == 0:
                col = random.randint(0, self.palette_length - 1)
                self.active_px[i] = self.palette[col]
                self.times[i] = context.clock

    def init_frame(self):
        frame = []
        for x in range(0, 64):
            frame.append((0, 0, 0))
        return frame

    @clocked(frames_per_second=24)
    def get_next_frame(self, context):
        # Read from weight input
        self.handle_weight_input(context)

        next_frame = self.init_frame()
        t = context.clock
        for x in range(0, 8):
            for y in range(0, 8):
                index = y * 8 + x
                if self.times[index] > 0:
                    age_scale = 1 - (t - self.times[index]) / self.LIFETIME
                    if age_scale < 0:
                        self.times[index] = 0
                    else:
                        next_pixel = color.scale_color(self.active_px[index], age_scale)
                        index = y * 8 + x
                        next_frame[index] = color.add_color(next_frame[index], next_pixel)
                        index = y * 8 + (7 - x)
                        next_frame[index] = color.add_color(next_frame[index], next_pixel)
                        index = (7 - y) * 8 + (7 - x)
                        next_frame[index] = color.add_color(next_frame[index], next_pixel)
                        index = (7 - y) * 8 + x
                        next_frame[index] = color.add_color(next_frame[index], next_pixel)
                        z = x
                        x = y
                        y = z
                        index = y * 8 + x
                        next_frame[index] = color.add_color(next_frame[index], next_pixel)
                        index = y * 8 + (7 - x)
                        next_frame[index] = color.add_color(next_frame[index], next_pixel)
                        index = (7 - y) * 8 + (7 - x)
                        next_frame[index] = color.add_color(next_frame[index], next_pixel)
                        index = (7 - y) * 8 + x
                        next_frame[index] = color.add_color(next_frame[index], next_pixel)

        return next_frame
