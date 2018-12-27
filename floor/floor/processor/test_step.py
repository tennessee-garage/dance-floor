from base import Base
from floor.util import color_utils


def create(args=None):
    return TestStep()


class TestStep(Base):

    MAX_WEIGHT = 40

    def __init__(self):
        super(TestStep, self).__init__()

    def get_next_frame(self, context):
        weights = context.weights
        pixels = []

        for idx in range(64):
            if idx < len(weights):
                w = weights[idx]
            else:
                w = 0

            val = color_utils.clamp(w, 0, 40)
            val = color_utils.remap(1.0 * val, 0, self.MAX_WEIGHT, 0, self.max_value)
            pixels.append((val, val, 0))

        return pixels
