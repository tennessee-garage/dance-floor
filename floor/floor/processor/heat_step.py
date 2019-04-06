from builtins import range
from floor.processor.base import Base
from floor.processor.utils import clocked


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

    CONTROLS = [
        {
            'name': 'HUE',
            'scale': 1.0,
            'default': 1.0
        },
        {
            'name': 'SAT',
            'scale': 1.0,
            'default': 1.0
        },
        # Good single steps for heat, cool: 3.5, 0.75
        # Good group steps for heat, cool: 20.5, 0.95
        {
            'name': 'HEAT',  # How much foot steps "heat" up the floor
            'range': [30.0, 3.5],
            'default': 20.0
        },
        {
            'name': 'COOL',  # How fast the floor "cools" over time
            'range': [0.95, 0.75],
            'default': 0.95
        }
    ]

    def __init__(self, **kwargs):
        super(HeatStep, self).__init__(**kwargs)
        self.pixels = self.zeroed_pixel_array()

        self.secondary_hue = 0.5
        self.value = 1.0

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
                scale = (DISTANCE[dist_y][dist_x]**2) * self.HEAT
                idx = (other_x * self.FLOOR_WIDTH) + other_y
                pixel = self.pixels[idx]

                # Set the hue and saturation of this heated square and increase or set the value
                pixel[0] = self.secondary_hue
                pixel[1] = self.SAT
                pixel[2] += self.value / scale

    def cool_floor(self):
        """Cool the floor every cycle"""
        for y in range(8):
            for x in range(8):
                idx = (x * self.FLOOR_WIDTH) + y
                pixel = self.pixels[idx]

                # Decrease the V of this HSV pixel
                pixel[2] *= self.COOL

    def set_secondary_hue(self):
        self.secondary_hue = self.HUE + 0.5
        if self.secondary_hue > 1.0:
            self.secondary_hue -= 1.0

    @clocked(frames_per_second=24)
    def get_next_frame(self, context):
        weights = context.weights
        self.set_secondary_hue()

        self.cool_floor()

        for y in range(8):
            for x in range(8):
                idx = (x * self.FLOOR_WIDTH) + y
                if weights[idx] > 0:
                    self.pixels[idx] = [self.HUE, self.SAT, self.value]
                    self.heat_squares(weights, x, y)

        return self.hsv_to_rgb_pixels(self.pixels)
