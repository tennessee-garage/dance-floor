import logging

from base import Base
from floor.controller import midi

logger = logging.getLogger('simple_step')

# Matrix of distances so we don't have to calculate them.  Distances
# are from the corner at 0, 0.  Can be reflected over x or y to give distance
# in the negative directions.
DISTANCE = [
    [0.00, 1.00, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00],
    [1.00, 1.41, 2.24, 3.16, 4.12, 5.10, 6.08, 7.07],
    [2.00, 2.24, 2.83, 3.61, 4.47, 5.39, 6.32, 7.28],
    [3.00, 3.16, 3.61, 4.24, 5.00, 5.83, 6.71, 7.62],
    [4.00, 4.12, 4.47, 5.00, 5.66, 6.40, 7.21, 8.06],
    [5.00, 5.10, 5.39, 5.83, 6.40, 7.07, 7.81, 8.60],
    [6.00, 6.08, 6.32, 6.71, 7.21, 7.81, 8.49, 9.22],
    [7.00, 7.07, 7.28, 7.62, 8.06, 8.60, 9.22, 9.90],
]


class HeatStep(Base):

    # Good single steps: 3.5, 0.75
    # Good group steps 20.5, 0.95
    HEAT_RANGE = [3.5, 30.0]
    COOL_RANGE = [0.75, 0.95]

    def __init__(self, **kwargs):
        super(HeatStep, self).__init__(**kwargs)
        self.pixels = self.zeroed_pixel_array()

        self.hue = 1.0
        self.secondary_hue = 0.5
        self.saturation = 1.0
        self.value = 1.0

        self.heat_factor = 20.5
        self.cool_factor = 0.95
        self.heat_delta = self.HEAT_RANGE[1] - self.HEAT_RANGE[0]
        self.cool_delta = self.COOL_RANGE[1] - self.COOL_RANGE[0]

    def handle_midi_command(self, command):
        if command[0] == midi.COMMAND_CONTROL_MODE_CHANGE:
            num = command[2]
            if command[1] == 48:
                self.adjust_hue(num)
            elif command[1] == 49:
                self.adjust_saturation(num)
            elif command[1] == 50:
                self.adjust_heating(num)
            elif command[1] == 51:
                self.adjust_cooling(num)

    def adjust_hue(self, num):
        self.hue = num / 127.0

        # Set the secondary hue to be 180 deg off the primary hue
        self.secondary_hue = self.hue + 0.5
        if self.secondary_hue > 1.0:
            self.secondary_hue -= 1.0

        logger.info("Set primary hue to {}/127".format(num))

    def adjust_saturation(self, num):
        self.saturation = num / 127.0
        logger.info("Set saturation to {}/127".format(num))

    def adjust_heating(self, num):
        """Adjust the heating within the range given by HEAT_RANGE

        Higher numbers actually mean lower "heating" since this factor is used as a
        factor dividing the max value.  So, we do 1 - num/127 to make sure the sliders
        act as "more heating" when pushed up.
        """
        self.heat_factor = self.HEAT_RANGE[0] + (1-(num/127.0))*self.heat_delta
        logger.info("Set heating to {0:.2f}".format(self.heat_factor))

    def adjust_cooling(self, num):
        """Adjust the cooling within the range given by COOL_RANGE

        Higher numbers actually mean slower "cooling" since this factor between 0.0 and 1.0
        is used as a percentage "heat" lost.  So, we do 1 - num/127 to make sure the sliders
        act as "more cooling" when pushed up.
        """
        self.cool_factor = self.COOL_RANGE[0] + (1-(num/127.0))*self.cool_delta
        logger.info("Set cooling to {0:.2f}".format(self.cool_factor))

    def heat_squares(self, weights, x, y):
        """Heat up squares based on proximity to step at x, y"""
        for other_y in range(8):
            for other_x in range(8):
                other_idx = (other_x * self.FLOOR_WIDTH) + other_y
                if weights[other_idx] > 0:
                    # Don't do anything if the square is already being pressed
                    continue

                dist_x = abs(x - other_x)
                dist_y = abs(y - other_y)
                if dist_x == 0 and dist_y == 0:
                    continue
                scale = (DISTANCE[dist_y][dist_x]**2) * self.heat_factor
                idx = (other_x * self.FLOOR_WIDTH) + other_y
                pixel = self.pixels[idx]

                # Set the hue and saturation of this heated square and increase or set the value
                pixel[0] = self.secondary_hue
                pixel[1] = self.saturation
                pixel[2] += self.value / scale

    def cool_floor(self):
        """Cool the floor every cycle"""
        for y in range(8):
            for x in range(8):
                idx = (x * self.FLOOR_WIDTH) + y
                pixel = self.pixels[idx]

                # Decrease the V of this HSV pixel
                pixel[2] *= self.cool_factor

    def get_next_frame(self, weights):
        self.cool_floor()

        for y in range(8):
            for x in range(8):
                idx = (x * self.FLOOR_WIDTH) + y
                if weights[idx] > 0:
                    self.pixels[idx] = [self.hue, self.saturation, self.value]
                    self.heat_squares(weights, x, y)

        return self.hsv_to_rgb_pixels(self.pixels)
