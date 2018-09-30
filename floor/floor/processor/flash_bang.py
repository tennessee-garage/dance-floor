from base import Base
import random
import math


class FlashBang(Base):

    # Random range for how long the main burst lasts
    BURST_DECAY_MAX = 0.95
    BURST_DECAY_MIN = 0.88

    # Random range for how intense the burst is
    BURST_INTENSITY_MAX = 1.0
    BURST_INTENSITY_MIN = 0.95

    # Random range for when the sparkles are triggered (as a percentage of the current burst level)
    SPARKLE_TRIGGER_MAX = 0.5
    SPARKLE_TRIGGER_MIN = 0.25

    # Percent chance (from 0.0 to 1.0) that a square will sparkle
    SPARKLE_PERCENT = 0.40
    SPARKLE_SPACING = 5

    def __init__(self, **kwargs):
        super(FlashBang, self).__init__(**kwargs)
        self.burst_pixels = []
        self.sparkles = []

        self.burst_finished = True
        self.burst_decay = self.BURST_DECAY_MAX
        self.burst_intensity = self.BURST_INTENSITY_MAX

        self.burst_red = self.max_value
        self.burst_green = self.max_value
        self.burst_blue = self.max_value

        self.sparkle_trigger = self.SPARKLE_TRIGGER_MAX * self.max_value
        self.sparkle_start = False
        self.sparkling = False

        self.init_burst_pixels()
        self.create_burst()

    def init_burst_pixels(self):
        for x in range(0, 64):
            self.burst_pixels.append([0, 0, 0])

    def set_burst_decay(self):
        # Randomly set the burst decay to something between BURST_DECAY_MAX and BURST_DECAY_MIN
        self.burst_decay = self.value_in_range(self.BURST_DECAY_MIN, self.BURST_DECAY_MAX)

    def set_burst_intensity(self):
        # Randomly set the burst intensity to something between BURST_INTENSITY_MAX and BURST_INTENSITY_MIN
        self.burst_intensity = self.value_in_range(self.BURST_INTENSITY_MIN, self.BURST_INTENSITY_MAX)

    @staticmethod
    def value_in_range(min_val, max_val):
        return min_val + random.random() * (max_val - min_val)

    def fade_burst(self):
        still_fading = False
        still_bright = False

        for rgb in self.burst_pixels:
            for color in range(0, 3):
                rgb[color] *= self.burst_decay
                if rgb[color] < 1.0:
                    rgb[color] = 0
                else:
                    # If any color is still above 1.0, we're still fading
                    still_fading = True

                # As long as any one color is above the trigger, we're still too bright
                if rgb[color] > self.sparkle_trigger:
                    still_bright = True

        if not still_fading:
            self.burst_finished = True

        if not still_bright:
            self.sparkle_start = True

    def create_burst(self):
        self.burst_finished = False
        self.sparkle_start = False
        self.sparkling = False
        self.clear_burst_pixels()

        burst_x = random.randint(0, 7)
        burst_y = random.randint(0, 7)
        self.burst_red = random.randint(int(self.max_value * 0.8), self.max_value*2)
        self.burst_green = random.randint(int(self.max_value * 0.8), self.max_value*2)
        self.burst_blue = random.randint(int(self.max_value * 0.8), self.max_value*2)

        for x in range(0, 8):
            for y in range(0, 8):
                power_factor = self.inverse_square(x, y, burst_x, burst_y)
                self.burst_pixels[y*8 + x] = [
                    self.burst_red * power_factor,
                    self.burst_green * power_factor,
                    self.burst_blue * power_factor
                ]

        self.set_sparkle_trigger()

    def set_sparkle_trigger(self):
        self.sparkle_trigger = ((self.burst_red + self.burst_green + self.burst_blue)/3)\
                               * self.value_in_range(self.SPARKLE_TRIGGER_MIN, self.SPARKLE_TRIGGER_MAX)

    def create_sparkles(self):
        self.sparkles = []
        for x in range(0, 64):
            if random.random() < self.SPARKLE_PERCENT:
                self.sparkles.append(-1 * random.randint(0, 24*3))
            else:
                self.sparkles.append(-99999)

    def clear_burst_pixels(self):
        for x in range(0, 64):
            self.burst_pixels[x] = [0, 0, 0]

    def append_burst_pixels(self, pixels):
        for x in range(0, 64):
            pixels.append(self.burst_pixels[x])

    def add_sparkles(self, pixels):
        for x in range(0, 64):
            # If the sparkle value is greater than zero and is a multiple of self.SPARKLE_SPACING then
            # start a sparkle!
            if (self.sparkles[x] > 0)\
                    and self.sparkles[x] < 24\
                    and (self.sparkles[x] % self.SPARKLE_SPACING == 0):
                pixels[x] = [self.burst_blue, self.burst_red, self.burst_green]
            self.sparkles[x] += 1
            self.burst_blue *= .9995
            self.burst_red *= .9995
            self.burst_green *= .9995

    @staticmethod
    def inverse_square(x, y, center_x, center_y):
        zoom = 0.065
        # Inverse square law is 1/distance**2.  Here distance is sqrt((x-center_x)**+(y-y_center)**2)
        # The square and and sqrt cancel out here and just give the following inverse:
        distance = math.sqrt((x*zoom - center_x*zoom)**2 + (y*zoom - center_y*zoom)**2)
        distance += 1

        if distance == 0:
            return 0
        else:
            return 1/(distance**2)

    def get_next_frame(self, weights):
        # Ignore weights

        pixels = []
        self.append_burst_pixels(pixels)
        self.fade_burst()

        # If sparkle_start is triggered and we're not already sparkling
        if self.sparkle_start and not self.sparkling:
            self.create_sparkles()
            self.sparkling = True

        if self.sparkling:
            self.add_sparkles(pixels)

        if self.burst_finished:
            self.create_burst()

        return pixels
