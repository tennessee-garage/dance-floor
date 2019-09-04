from builtins import range
from floor.processor.base import Base


class SimpleStep(Base):

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
        {
            'name': 'VAL',
            'scale': 1.0,
            'default': 1.0
        }
    ]

    def __init__(self, **kwargs):
        super(SimpleStep, self).__init__(**kwargs)

    def get_next_frame(self, context):
        weights = context.weights
        pixels = [(0, 0, 0)] * 64

        for idx in range(64):
            if weights[idx] > 0:
                pixels[idx] = self.hsv_to_rgb([self.HUE, self.SAT, self.VAL])

        return pixels
