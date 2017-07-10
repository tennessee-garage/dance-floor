from base import Base
import math
import random


def create(args=None):
    return Electricity()


class Electricity(Base):

    DECAY_RATE = 0.8
    DECAY_THRESHOLD = 0.001

    def __init__(self):
        super(Electricity, self).__init__()
        self.arc = Arc(1, 63)

        self.pixels = []
        for idx in range(0, 64):
            self.pixels.append([0, 0, 0])

    def get_next_frame(self, weights):
        self.fade_frame()
        self.arc.advance()
        for idx, val in enumerate(self.arc.frame):
            if val > 0:
                self.pixels[idx] = [val*self.max_value, val*self.max_value, val*self.max_value]

        return self.pixels

    def fade_frame(self):
        for idx in range(0, 64):
            if self.pixels[idx][0] > self.DECAY_THRESHOLD:
                self.pixels[idx][0] *= self.DECAY_RATE
                self.pixels[idx][1] *= self.DECAY_RATE
                self.pixels[idx][2] *= self.DECAY_RATE
            else:
                self.pixels[idx] = [0, 0, 0]


class Arc(object):

    LEAD_PATH = 1.0
    LEAD_ALTERNATE = 0.4

    def __init__(self, point1, point2):
        # Two points on the floor to arc between
        self.point1 = point1
        self.point2 = point2

        # The points translated to x & y
        self.p1x = point1 % 8
        self.p1y = int(point1 / 8)
        self.p2x = point2 % 8
        self.p2y = int(point2 / 8)

        # The position of the leading edge of the arc
        self.lead_x = self.p1x
        self.lead_y = self.p1y

        # The distance between the start and end point
        self.cur_distance = 0

        # Whether the arc has connected
        self.connected = False

        # Hold the arc pattern
        self.frame = []
        for idx in range(0, 64):
            self.frame.append(0)

    def advance(self):
        options = []
        self.set_cur_distance()

        # Upper left
        self.add_if_valid(options, self.lead_x - 1, self.lead_y - 1)

        # Upper center
        self.add_if_valid(options, self.lead_x, self.lead_y - 1)

        # Upper right
        self.add_if_valid(options, self.lead_x + 1, self.lead_y - 1)

        # Middle right
        self.add_if_valid(options, self.lead_x + 1, self.lead_y)

        # Lower right
        self.add_if_valid(options, self.lead_x + 1, self.lead_y + 1)

        # Lower middle
        self.add_if_valid(options, self.lead_x, self.lead_y + 1)

        # Lower left
        self.add_if_valid(options, self.lead_x - 1, self.lead_y + 1)

        # Middle left
        self.add_if_valid(options, self.lead_x - 1, self.lead_y)

        pick = random.randint(0, len(options) - 1)
        for idx, point in enumerate(options):
            if idx == pick:
                self.frame[point[0] + point[1]*8] = self.LEAD_PATH
                self.lead_x = point[0]
                self.lead_y = point[1]
            else:
                self.frame[point[0] + point[1] * 8] = self.LEAD_ALTERNATE

        if self.connected:
            # Start over again
            self.lead_x = self.p1x
            self.lead_y = self.p1y
            self.clear_frame()
            self.connected = False

    def set_cur_distance(self):
        self.cur_distance = self.dist_to_p2(self.lead_x, self.lead_y)

    def add_if_valid(self, options, x, y):
        d = self.dist_to_p2(x, y)
        if d != -1 and d < self.cur_distance:
            options.append((x, y))
        if d == 0:
            self.connected = True

    def dist_to_p2(self, x, y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return -1

        return math.sqrt((x - self.p2x)**2 + (y - self.p2y)**2)

    def clear_frame(self):
        for idx in range(0, 64):
            self.frame[idx] = 0.0
