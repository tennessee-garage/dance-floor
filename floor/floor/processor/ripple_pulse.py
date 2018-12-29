import math
from utils import clocked

from ripple import Ripple


class RipplePulse(Ripple):

    # 0.75 is good for long pulses
    DECAY = 4
    OMEGA = 2 * math.pi

    # How much distance translates the time value sent to the decay method.
    # A number between 0.02 and 0.18 seems to look best.
    #  - Lower than 0.02 and the whole floor seems to flash at once
    #  - higher than 0.18 and there are too many striations and it looks noisy, not smooth
    DISTANCE_FACTOR = 0.03

    def __init__(self, **kwargs):
        super(RipplePulse, self).__init__(**kwargs)

    @clocked(frames_per_beat=.5)
    def reset_on_beat(self, context):
        self.t_start = context.clock
        self.hue += self.hue_rotation
        if self.hue > 1.0:
            self.hue -= 1.0
