import logging
import colorsys

from base import Base
from floor.controller import midi

logger = logging.getLogger('simple_step')


class SimpleStep(Base):
    HUE_SLIDER = 48
    SAT_SLIDER = 49
    VAL_SLIDER = 50

    def __init__(self, **kwargs):
        super(SimpleStep, self).__init__(**kwargs)
        self.hue = 1.0
        self.saturation = 1.0
        self.value = 1.0
        self.red = self.max_value
        self.green = 0
        self.blue = 0

    def handle_midi_command(self, command):
        if command[0] == midi.COMMAND_CONTROL_MODE_CHANGE:
            value = command[2]
            if command[1] == self.HUE_SLIDER:
                self.hue = value/127.0
                logger.info("Set hue to {}/127".format(value))
            if command[1] == self.SAT_SLIDER:
                self.saturation = value/127.0
                logger.info("Set saturation to {}/127".format(value))
            if command[1] == self.VAL_SLIDER:
                self.value = value/127.0
                logger.info("Set value to {}/127".format(value))

            self.red, self.green, self.blue = self.hsv_to_rgb([self.hue, self.saturation, self.value])

    def get_next_frame(self, weights):
        pixels = [(0, 0, 0)] * 64

        for idx in range(64):
            if weights[idx] > 0:
                pixels[idx] = (self.red, self.green, self.blue)

        return pixels
