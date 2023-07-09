import random
from builtins import range

from floor.processor.base import Base
from floor.processor.constants import COLOR_MAXIMUM
from floor.processor.utils import clocked


class Pulsar(Base):
    def __init__(self, **kwargs):
        super(Pulsar, self).__init__(**kwargs)
        self.pixels = []
        self.wave_toggle = 1
        self.last_time = None

        for x in range(0, 8):
            for y in range(0, 8):
                self.pixels.append((0, 0, 0))

    def neighbor_sum(self, x, y, i):
        # anti_alias < 1 will round corners. leaving it at 1 for now, the rectangle patterns are nice
        anti_alias = 1.0
        px = self.pixels
        sum = 0
        if x > 0:
            # middle-left
            sum += px[y * 8 + (x - 1)][i]
            if y > 0:
                # top-left
                sum += anti_alias * px[(y - 1) * 8 + (x - 1)][i]
            if y < 7:
                # bottom-left
                sum += anti_alias * px[(y + 1) * 8 + (x - 1)][i]
        if x < 7:
            # middle-right
            sum += px[y * 8 + (x + 1)][i]
            if y > 0:
                # top-right
                sum += anti_alias * px[(y - 1) * 8 + (x + 1)][i]
            if y < 7:
                # bottom-right
                sum += anti_alias * px[(y + 1) * 8 + (x + 1)][i]

        if y > 0:
            # top-middle
            sum += px[(y - 1) * 8 + x][i]
        if y < 7:
            # bottom-middle
            sum += px[(y + 1) * 8 + x][i]

        # we're not wrapping, and we add a little extra decay factor at the edges
        if x == 0 or y == 0 or x == 7 or y == 7:
            sum *= 0.9

        return sum

    def handle_weight_input(self, weights):
        # Weight values are either 0 or 1.  If 1 consider it a step and add a pixel
        for i in range(0, 64):
            if weights[i] > 0:
                self.pixels[i] = (
                    COLOR_MAXIMUM * random.random(),
                    COLOR_MAXIMUM * random.random(),
                    COLOR_MAXIMUM * random.random(),
                )

    def random_weight_input(self):
        count = random.randint(1, 5)
        for i in range(0, count):
            # index: pick a random square for the source
            index = random.randint(0, 63)
            self.pixels[index] = (
                COLOR_MAXIMUM * random.random(),
                COLOR_MAXIMUM * random.random(),
                COLOR_MAXIMUM * random.random(),
            )

    @clocked(frames_per_second=24)
    def get_next_frame(self, context):
        weights = context.weights

        if self.last_time is None:
            self.last_time = context.clock
        next_time = context.clock

        # reset_time could be beat driven
        reset_time = 1.2

        # Read from weight input
        self.handle_weight_input(weights)

        # whenever we hit the reset time, wipe the board and choose more sources
        if next_time - self.last_time > reset_time:
            self.pixels = []
            self.last_time = next_time
            self.wave_toggle = 1
            self.pixels = []
            for y in range(0, 8):
                for x in range(0, 8):
                    self.pixels.append((0, 0, 0))

            # Uncomment to have random weight inputs
        #            self.random_weight_input()

        # after a certain amount of time, toggle wave direction and make it recede, but weakly
        elif (next_time - self.last_time) > (0.5 * reset_time):
            self.wave_toggle = -0.2

        # propagate the blossoms
        self_decay = 0.9
        wave_decay = 0.5
        adjusted_max = 0.8 * COLOR_MAXIMUM

        next_pixels = []
        for y in range(0, 8):
            for x in range(0, 8):
                last_pixel = self.pixels[y * 8 + x]
                next_red = self_decay * (
                    last_pixel[0] + self.wave_toggle * wave_decay * self.neighbor_sum(x, y, 0) / 8
                )
                next_blue = self_decay * (
                    last_pixel[1] + self.wave_toggle * wave_decay * self.neighbor_sum(x, y, 1) / 8
                )
                next_green = self_decay * (
                    last_pixel[2] + self.wave_toggle * wave_decay * self.neighbor_sum(x, y, 2) / 8
                )

                if next_red > adjusted_max:
                    next_red = adjusted_max
                if next_blue > adjusted_max:
                    next_blue = adjusted_max
                if next_green > adjusted_max:
                    next_green = adjusted_max
                next_pixel = (next_red, next_blue, next_green)

                next_pixels.append(next_pixel)

        self.pixels = next_pixels

        return self.pixels
