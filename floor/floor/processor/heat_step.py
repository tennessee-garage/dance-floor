import logging
import colorsys

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

    # good single steps: 3.5, 0.75

    HEAT_FACTOR = 20.5
    COOL_FACTOR = 0.95

    def __init__(self, **kwargs):
        super(HeatStep, self).__init__(**kwargs)
        self.pixels = self.zeroed_pixel_array()

        self.hue = 1.0
        self.saturation = 1.0
        self.value = 1.0
        self.red = self.max_value
        self.green = 0
        self.blue = 0

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
                scale = (DISTANCE[dist_y][dist_x]**2) * self.HEAT_FACTOR
                idx = (other_x * self.FLOOR_WIDTH) + other_y
                pixel = self.pixels[idx]

                pixel[0] += int(self.red / scale)
                if pixel[0] > self.red:
                    pixel[0] = self.red

                pixel[1] += int(self.green / scale)
                if pixel[1] > self.green:
                    pixel[1] = self.green

                pixel[2] += int(self.blue / scale)
                if pixel[2] > self.blue:
                    pixel[2] = self.blue

    def cool_floor(self):
        """Cool the floor every cycle"""
        for y in range(8):
            for x in range(8):
                idx = (x * self.FLOOR_WIDTH) + y
                pixel = self.pixels[idx]
                pixel[0] *= self.COOL_FACTOR
                pixel[1] *= self.COOL_FACTOR
                pixel[2] *= self.COOL_FACTOR

    def get_next_frame(self, weights):
        self.cool_floor()

        for y in range(8):
            for x in range(8):
                idx = (x * self.FLOOR_WIDTH) + y
                if weights[idx] > 0:
                    self.pixels[idx] = [self.blue, self.green, self.red]
                    self.heat_squares(weights, x, y)

        return self.pixels
