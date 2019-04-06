from builtins import range
from builtins import object
import random

from floor.processor.base import Base
from floor.processor.utils import clocked
from floor.util import color_utils
from floor.processor.constants import COLOR_MAXIMUM


class Stripes(Base):
    DEFAULT_FADE_LENGTH = 100

    DEFAULT_MAX_SPEED = 1.0
    DEFAULT_MIN_SPEED = 0.2

    def __init__(self, **kwargs):
        super(Stripes, self).__init__(**kwargs)
        self.palette = color_utils.get_random_palette(COLOR_MAXIMUM)
        self.gradient = [[] for _ in range(len(self.palette))]
        self.stripes = [None for _ in range(8)]  # list[Stripe]

        fade_length = kwargs.get("length", self.DEFAULT_FADE_LENGTH)
        self.max_speed = kwargs.get("max_speed", self.DEFAULT_MAX_SPEED)
        self.min_speed = kwargs.get("min_speed", self.DEFAULT_MIN_SPEED)

        for idx, p in enumerate(self.palette):
            for n in range(fade_length, 1, -1):
                fade_factor = 1.0/n
                self.gradient[idx].append((p[0]*fade_factor, p[1]*fade_factor, p[2]*fade_factor))

            self.gradient[idx].append(p)

            for n in range(2, fade_length+1):
                fade_factor = 1.0/n
                self.gradient[idx].append((p[0]*fade_factor, p[1]*fade_factor, p[2]*fade_factor))

        for idx in range(8):
            self.stripes[idx] = self.generate_new_stripe()

    def generate_new_stripe(self):
        num_gradients = len(self.gradient)
        gradient = self.gradient[int(random.random() * num_gradients)]
        speed = random.uniform(self.min_speed, self.max_speed)
        if random.random() > 0.5:
            direction = 1
        else:
            direction = -1

        return Stripe(gradient, speed, direction)

    @clocked(frames_per_second=24)
    def get_next_frame(self, context):
        pixels = []

        for row in range(0, 8):
            stripe = self.stripes[row]
            values = stripe.get_values()

            pixels.extend(values)

            if stripe.is_done():
                self.stripes[row] = self.generate_new_stripe()
            else:
                stripe.advance()

        return pixels


class Stripe(object):

    def __init__(self, gradient, speed, direction):
        self.gradient = gradient
        self.speed = speed
        self.direction = direction

        self.buffer = [(0, 0, 0) for _ in range(8)]
        self.buffer.extend(self.gradient)
        self.buffer.extend([(0, 0, 0) for _ in range(8)])

        self.done = False

        if self.direction > 0:
            self.start = 0
        else:
            self.start = len(self.buffer) - 8

    def get_values(self):
        return self.buffer[int(self.start):int(self.start)+8]

    def is_done(self):
        return self.done

    def advance(self):
        if self.done:
            return

        if self.direction > 0:
            self.start += self.speed
            if int(self.start) >= len(self.buffer) - 8:
                self.done = True
                self.start = len(self.buffer) - 8
        else:
            self.start -= self.speed
            if int(self.start) <= 0:
                self.done = True
                self.start = 0
