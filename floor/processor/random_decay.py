from base import Base
import random

def create():
    return RandomDecay()


class RandomDecay(Base):
    def __init__(self):
        super(RandomDecay, self).__init__()
        self.red = 0
        self.green = 0
        self.blue = 0
        self.pixels = [];

        for x in range(0, 8):
            for y in range(0, 8):
                self.pixels.append((
                    self.max_value*random.random(),
                    self.max_value*random.random(),
                    self.max_value*random.random()
                ))

    def get_next_frame(self, weights):
        next_pixels = []
        decay_rate = 0.9

        for x in range(0, 8):
            for y in range(0, 8):
                next_pixel = self.pixels[x*8 + y]
                next_red = decay_rate*next_pixel[0]
                next_blue = decay_rate*next_pixel[1]
                next_green = decay_rate*next_pixel[2]
                if (next_red + next_blue + next_green) < 10:
                    next_red = self.max_value*random.random()
                    next_blue = self.max_value*random.random()
                    next_green = self.max_value*random.random()
                next_pixels.append((
                    next_red,
                    next_blue,
                    next_green
                ))

        self.pixels = next_pixels

        return self.pixels
