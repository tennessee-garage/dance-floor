import random
import math

from floor.processor.base import Base
from floor.processor.utils import clocked
from floor.processor.constants import COLOR_MAXIMUM


class Balls(Base):
    """Spiral out from the center."""

    def __init__(self, **kwargs):
        super(Balls, self).__init__(**kwargs)

        self.count = 0.0
        self.count_delta = 0.1
        self.spawn_chance = 0.3

        self.max_in_flight = 20
        self.in_flight = []

    def rand_color(self):
        return [random.randrange(COLOR_MAXIMUM),
                random.randrange(COLOR_MAXIMUM),
                random.randrange(COLOR_MAXIMUM)]

    def can_spawn_ball(self):
        """Max self.spawn_chance chance of spawning a ball, modulated by a sine curve.
        """
        val = random.random() * (math.sin(self.count) + 1.0)
#        print "Val = {}".format(val)
        return val > self.spawn_chance

    @clocked(frames_per_second=24)
    def get_next_frame(self, context):
        pixels = [[0 for _ in range(3)] for _ in range(64)]

        if len(self.in_flight) < self.max_in_flight:
            if self.can_spawn_ball():
                ball = Ball(row=random.randrange(8), delta=0.08, decay=0.85, color=self.rand_color())
                self.in_flight.append(ball)

        remaining = []
        for ball in self.in_flight:
            row_pos = int(round(ball.position))
            if row_pos <= 7:
                index = int(round(ball.position)) + (ball.row*8)
                pixels[index] = ball.color

            ball.run()

            if not ball.finished:
                remaining.append(ball)

        self.in_flight = remaining
        self.count += self.count_delta

        return pixels


class Ball(object):

    def __init__(self, row, delta, decay, color):
        self.t = 0

        self.row = row
        self.delta = delta
        self.decay = decay

        self.start_position = 15
        self.max_height = 0.0
        self.position = 7
        self.color = color
        self.v = 0

        self.finished = False

    def run(self):
        self.position = self.start_position + (self.v * self.t) + (-9.8 * self.t**2)
        self.max_height = max(self.max_height, self.position)

#        print "t={}, p={}, v={}".format(self.t, self.position, self.v)

        if self.position < 0.0:
            if self.max_height < 0.5:
                self.finished = True
                return

            self.max_height = 0.0
#            self.v = math.sqrt(2 * 9.8 * self.start_position)
            self.start_position = 0.0
            self.position = 0.0
            self.v = 9.8 * self.t * self.decay

            self.t = 0.0

#            print "bounce: t={}, p={}, v={}".format(self.t, self.position, self.v)

        self.t += self.delta
