import colorsys
import math
import time
from utils import clocked

from base import Base


# The distance from the center for every square
DISTANCE = [
    4.95, 4.30, 3.81, 3.54, 3.54, 3.81, 4.30, 4.95,
    4.30, 3.54, 2.92, 2.55, 2.55, 2.92, 3.54, 4.30,
    3.81, 2.92, 2.12, 1.58, 1.58, 2.12, 2.92, 3.81,
    3.54, 2.55, 1.58, 0.71, 0.71, 1.58, 2.55, 3.54,
    3.54, 2.55, 1.58, 0.71, 0.71, 1.58, 2.55, 3.54,
    3.81, 2.92, 2.12, 1.58, 1.58, 2.12, 2.92, 3.81,
    4.30, 3.54, 2.92, 2.55, 2.55, 2.92, 3.54, 4.30,
    4.95, 4.30, 3.81, 3.54, 3.54, 3.81, 4.30, 4.95
]


class Ripple(Base):
    """Spiral out from the center."""

    # 0.75 is good for long pulses
    DECAY = 0.75
    OMEGA = 2 * math.pi
    # How much distance translates the time value sent to the decay method.
    # A number between 0.02 and 0.18 seems to look best.
    #  - Lower than 0.02 and the whole floor seems to flash at once
    #  - higher than 0.18 and there are too many striations and it looks noisy, not smooth
    DISTANCE_FACTOR = 0.03

    RESTART_THRESHHOLD = 0.01

    def __init__(self, **kwargs):
        super(Ripple, self).__init__(**kwargs)
        self.t_start = None
        self.hue = 0.0
        self.hue_rotation = 0.05

    def requested_fps(self):
        return 120

    @clocked(frames_per_beat=0.125)
    def reset_on_beat(self):
        self.t_start = time.time()
        self.hue += self.hue_rotation
        if self.hue > 1.0:
            self.hue -= 1.0

    def get_next_frame(self, weights):
        now = time.time()

        if self.t_start is None:
            self.t_start = now

        # Enact a reset whenever a beat hits
        self.reset_on_beat()

        pixels = []
        for dist in DISTANCE:
            factor = self.sin_decay((now-self.t_start) - dist*self.DISTANCE_FACTOR)
            if factor > 1.0:
                factor = 0.0

            if factor > 0:
                r, g, b = colorsys.hsv_to_rgb(self.hue, 1.0, factor)
            else:
                r, g, b = colorsys.hsv_to_rgb(self.hue, 0.5, -1 * factor)

            pixels.append([r * self.max_value, g * self.max_value, b * self.max_value])

        return pixels

    def sin_decay(self, t):
        """
        Calculates decay for given point in time.

        Equation for exponential sinusoidal decay

            y(t)=A * e^(-lambda * t) * cos(omega * t + phi )

        Here:
            t = time
            A = initial amplitude which will be 1.0 (applied as a scaling value to intensity)
            lambda = decay constant
            omega = angular frequency
            phi = phase angle at t=0 which for us will be 0.0
        """
        return (math.e**(-self.DECAY * t)) * math.cos(self.OMEGA * t)
