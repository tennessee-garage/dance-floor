from floor.processor.base import Base
from floor.processor.utils import clocked


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
        self.hue = 1.0
        self.saturation = 1.0
        self.value = 1.0
        self.red = self.max_value
        self.green = 0
        self.blue = 0

    @clocked(frames_per_second=24)
    def get_next_frame(self, context):
        weights = context.weights
        pixels = [(0, 0, 0)] * 64

        for idx in range(64):
            if weights[idx] > 0:
                pixels[idx] = self.hsv_to_rgb([self.HUE, self.SAT, self.VAL])

        return pixels
