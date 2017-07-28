from base import Base
from util import color_utils


def create(args=None):
    return TestStep()


class TestStep(Base):
    def __init__(self):
        super(TestStep, self).__init__()

    def get_next_frame(self, weights):

        pixels = []

        for idx in range(64):
            if idx < len(weights):
                w = weights[idx]
            else:
                w = 0

            val = color_utils.clamp(w, 0, 50)
            val = color_utils.remap(val, 0, 50, 0, self.max_value)
            pixels.append((val, val, 0))

        return pixels
