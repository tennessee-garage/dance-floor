import colorsys
import math

from floor.processor.base import Base
from floor.processor.utils import clocked
from floor.processor.constants import COLOR_MAXIMUM


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

    CONTROLS = [
        # Scale how far squares are from each other
        {
            'name': 'DISTANCE_FACTOR',
            'range': [0.02, 0.18],
            'default': 0.03
        },
        # How quickly do we dampen the waves
        {
            'name': 'DECAY',
            'range': [0.25, 2.0],
            'default': 0.75
        },

    ]

    OMEGA = 2 * math.pi
    RESTART_THRESHOLD = 0.01

    def __init__(self, **kwargs):
        super(Ripple, self).__init__(**kwargs)
        self.t_start = None
        self.hue = 0.0
        self.hue_rotation = 0.05

    @clocked(frames_per_beat=0.125)
    def reset_on_beat(self, context):
        self.t_start = context.clock
        self.hue += self.hue_rotation
        if self.hue > 1.0:
            self.hue -= 1.0

    @clocked(frames_per_second=120)
    def get_next_frame(self, context):
        now = context.clock

        if self.t_start is None:
            self.t_start = now

        # Enact a reset whenever a beat hits
        self.reset_on_beat(context)

        pixels = []
        for dist in DISTANCE:
            factor = self.sin_decay((now-self.t_start) - dist*self.DISTANCE_FACTOR)
            if factor > 1.0:
                factor = 0.0

            if factor > 0:
                r, g, b = colorsys.hsv_to_rgb(self.hue, 1.0, factor)
            else:
                r, g, b = colorsys.hsv_to_rgb(self.hue, 0.5, -1 * factor)

            pixels.append([r * COLOR_MAXIMUM, g * COLOR_MAXIMUM, b * COLOR_MAXIMUM])

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
