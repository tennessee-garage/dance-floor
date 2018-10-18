import math
import time


class Easing(object):

    def __init__(self, duration, start, end=None, change=None):
        self.t_start = None
        self.t = None
        self.delta = None
        self.v = None

        self.d = duration
        self.b = start
        if end:
            self.c = end-start
        elif change:
            self.c = change
        else:
            raise AttributeError('Easing need either end or change defined')

    def mark(self):
        # Initialize t_start if this easing has been reset or is new
        self.t_start = self.t_start or time.time()

        self.t = time.time()
        self.delta = self.t - self.t_start

        # Make sure we don't go beyond our duration
        if self.delta > self.d:
            self.delta = self.d

    def is_finished(self):
        if self.delta is None:
            return False
        return self.delta >= self.d

    def reset(self):
        self.t_start = None

    def reset_if_done(self):
        if self.is_finished():
            self.reset()

    def linear_tween(self):
        self.v = self.c * self.delta / self.d + self.b
        return self.v

    def ease_in_quad(self):
        t = self.delta / self.d
        self.v = self.c * t**2 + self.b
        return self.v

    def ease_out_quad(self):
        t = self.delta / self.d
        self.v = -self.c * t * (t - 2) + self.b
        return self.v

    def ease_in_out_quad(self):
        t = self.delta / self.d / 2
        if t < 1:
            self.v = self.c / 2 * t**2 + self.b
            return self.v
        t -= 1
        self.v = -self.c / 2 * (t * (t - 2) - 1) + self.b
        return self.v

    def ease_in_cubic(self):
        t = self.delta / self.d
        self.v = self.c * t**3 + self.b
        return self.v

    def ease_out_cubic(self):
        t = (self.delta / self.d) - 1
        self.v = self.c * (t**3 + 1) + self.b
        return self.v

    def ease_in_out_cubic(self):
        t = self.delta / self.d / 2
        if t < 1:
            self.v = self.c / 2 * t**3 + self.b
            return self.v
        t -= 2
        self.v = self.c / 2 * (t**3 + 2) + self.b
        return self.v

    def ease_in_quart(self):
        t = self.delta / self.d
        self.v = self.c * t**4 + self.b
        return self.v

    def ease_out_quart(self):
        t = self.delta / self.d
        t -= 1
        self.v = -self.c * (t**4 - 1) + self.b
        return self.v

    def ease_in_out_quart(self):
        t = self.delta / self.d / 2
        if t < 1:
            self.v = self.c / 2 * t**4 + self.b
            return self.v
        t -= 2
        self.v = -self.c / 2 * (t**4 - 2) + self.b
        return self.v

    def ease_in_quint(self):
        t = self.delta / self.d
        self.v = self.c * t**5 + self.b
        return self.v

    def ease_out_quint(self):
        t = (self.delta / self.d) - 1
        self.v = self.c * (t**5 + 1) + self.b
        return self.v

    def ease_in_out_quint(self):
        t = self.delta / self.d / 2
        if t < 1:
            self.v = self.c / 2 * t**5 + self.b
            return self.v
        t -= 2
        self.v = self.c / 2 * (t**5 + 2) + self.b
        return self.v

    def ease_in_sine(self):
        t = self.delta
        self.v = -self.c * math.cos(t / self.d * (math.pi / 2)) + self.c + self.b
        return self.v

    def ease_out_sine(self):
        t = self.delta
        self.v = self.c * math.sin(t / self.d * (math.pi / 2)) + self.b
        return self.v

    def ease_in_out_sine(self):
        t = self.delta
        self.v = -self.c / 2 * (math.cos(math.pi * t / self.d) - 1) + self.b
        return self.v

    def ease_in_expo(self):
        t = self.delta
        self.v = self.c * math.pow(2, 10 * (t / self.d - 1)) + self.b
        return self.v

    def ease_out_expo(self):
        t = self.delta
        self.v = self.c * (-math.pow(2, -10 * t / self.d) + 1) + self.b
        return self.v

    def ease_in_out_expo(self):
        t = self.delta / self.d / 2
        if t < 1:
            self.v = self.c / 2 * math.pow(2, 10 * (t - 1)) + self.b
            return self.v
        t -= 1
        self.v = self.c / 2 * (-math.pow(2, -10 * t) + 2) + self.b
        return self.v

    def ease_in_circ(self):
        t = self.delta / self.d
        self.v = -self.c * (math.sqrt(1 - t**2) - 1) + self.b
        return self.v

    def ease_out_circ(self):
        t = (self.delta / self.d) - 1
        self.v = self.c * math.sqrt(1 - t * t) + self.b
        return self.v

    def ease_in_out_circ(self):
        t = self.delta / self.d / 2
        if t < 1:
            self.v = -self.c / 2 * (math.sqrt(1 - t**2) - 1) + self.b
            return self.v
        t -= 2
        self.v = self.c / 2 * (math.sqrt(1 - t**2) + 1) + self.b
        return self.v
