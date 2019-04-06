from builtins import range
from floor.processor.base import Base
from floor.processor.utils import clocked
from floor.util import color_utils
from floor.processor.constants import COLOR_MAXIMUM


def create(args=None):
    return TestStep()


class TestStep(Base):

    MAX_WEIGHT = 40

    def __init__(self):
        super(TestStep, self).__init__()

    @clocked(frames_per_second=24)
    def get_next_frame(self, context):
        weights = context.weights
        pixels = []

        for idx in range(64):
            if idx < len(weights):
                w = weights[idx]
            else:
                w = 0

            val = color_utils.clamp(w, 0, 40)
            val = color_utils.remap(1.0 * val, 0, self.MAX_WEIGHT, 0, COLOR_MAXIMUM)
            pixels.append((val, val, 0))

        return pixels
