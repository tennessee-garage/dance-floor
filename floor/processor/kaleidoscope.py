from base import Base
import time
import random
import math

def create():
    return Kaleidoscope()


class Kaleidoscope(Base):

    LIFETIME = 1.0

    def __init__(self):
        super(Kaleidoscope, self).__init__()
        self.active_px = []
        self.times = []

        for x in range(0, 64):
            self.active_px.append((0, 0, 0))
            self.times.append(0)


    def handle_weight_input(self, weights):
        # Weight values are either 0 or 1.  If 1 consider it a step and add a pixel
        for i in range(0, 64):
            if weights[i] > 0 and self.times[i]==0:
                self.active_px[i] = (
                    self.max_value * random.random(),
                    self.max_value * random.random(),
                    self.max_value * random.random())
                self.times[i] = time.time()
    def init_frame(self):
        frame = []
        for x in range(0, 64):
            frame.append((0, 0, 0))
        return frame


    def normalize_color(self, color):
        magnitude = math.sqrt(color[0]*color[0]+ color[1]*color[1] + color[2]*color[2])
        if magnitude > 0:
            scale =self.max_value / magnitude
            color = (scale*color[0], scale*color[1], scale*color[2])
        return color

    def add_color(self, color1, color2):
        return (color1[0]+color2[0], color1[1]+color2[1], color1[2]+color2[2])

    def scale_color(self, color, scale):
        return (scale*color[0], scale*color[1], scale*color[2])

    def get_next_frame(self, weights):

        # Read from weight input
        self.handle_weight_input(weights)

        next_frame = self.init_frame()
        t = time.time()
        for x in range(0, 8):
            for y in range(0, 8):
                index = y*8 + x
                if self.times[index] > 0:
                    age_scale = 1 - (t - self.times[index])/self.LIFETIME
                    if age_scale <0:
                        self.times[index] = 0
                    else:
                        next_pixel = self.scale_color(self.active_px[index], age_scale)
                        index = y*8 + x
                        next_frame[index] = self.add_color(next_frame[index], next_pixel)
                        index = y*8 + (7-x)
                        next_frame[index] = self.add_color(next_frame[index], next_pixel)
                        index = (7-y)*8 + (7-x)
                        next_frame[index] = self.add_color(next_frame[index], next_pixel)
                        index = (7-y)*8 + x
                        next_frame[index] = self.add_color(next_frame[index], next_pixel)
                        z = x
                        x = y
                        y = z
                        index = y*8 + x
                        next_frame[index] = self.add_color(next_frame[index], next_pixel)
                        index = y*8 + (7-x)
                        next_frame[index] = self.add_color(next_frame[index], next_pixel)
                        index = (7-y)*8 + (7-x)
                        next_frame[index] = self.add_color(next_frame[index], next_pixel)
                        index = (7-y)*8 + x
                        next_frame[index] = self.add_color(next_frame[index], next_pixel)

        # for x in range(0, 63):
        #    next_frame[x] = self.normalize_color(next_frame[x])

        return next_frame
