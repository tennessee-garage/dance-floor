from base import Base
import random
from random import randint

import time

def create():
    return Pulsar()


class Pulsar(Base):
    def __init__(self):
        super(Pulsar, self).__init__()
        self.red = 0
        self.green = 0
        self.blue = 0
        self.pixels = []
        self.last_drop = -1

        self.last_time = time.time()

        for x in range(0, 8):
            for y in range(0, 8):
                self.pixels.append((0, 0, 0))

    def neighbor_sum(self, x, y, i):
        px = self.pixels
        sum = 0
        if x>0:
            #middle-left
            sum += px[y*8 + (x-1)][i]
            if y>0:
                #top-left
                sum += px[(y-1)*8 + (x-1)][i]
            if y<7:
                #bottom-left
                sum += px[(y+1)*8 + (x-1)][i]
        if x<7:
            #middle-right
            sum += px[y*8 + (x+1)][i]
            if y>0:
                #top-right
                sum += px[(y-1)*8 + (x+1)][i]
            if y<7:
                #bottom-right
                sum += px[(y+1)*8 + (x+1)][i]

        if y>0:
            #top-middle
            sum += px[(y-1)*8 + x][i]
        if y<7:
            #bottom-middle
            sum += px[(y+1)*8 + x][i]

        #if x==0 or y==0 or x==7 or y==7:
        #    sum /= 1.5

        return sum

    def get_next_frame(self, weights):
        next_pixels = []
        next_time = time.time()

        if next_time - self.last_time > 1.2:
            self.last_time = next_time
            for y in range(0, 8):
                for x in range(0, 8):
                    next_pixels.append((0, 0, 0))

            self.last_drop = randint(0, 63)
            next_pixels[self.last_drop] = (
                                self.max_value*random.random(),
                                self.max_value*random.random(),
                                self.max_value*random.random())

        else :
            self_decay = 0.8;
            wave_decay = 0.45;
            max = 220

            for y in range(0, 8):
                for x in range(0, 8):
                    last_pixel = self.pixels[y*8 + x];
                    next_red = 1 * (self_decay * last_pixel[0] + wave_decay * self.neighbor_sum(x, y, 0) / 8)
                    next_blue = 1 * (self_decay * last_pixel[1] + wave_decay * self.neighbor_sum(x, y, 1) / 8)
                    next_green = 1 * (self_decay * last_pixel[2] + wave_decay * self.neighbor_sum(x, y, 2) / 8)
                    if next_red > max:
                        next_red = max
                    if next_blue > max:
                        next_blue = max
                    if next_green > max:
                        next_green = max
                    next_pixel = (next_red, next_blue, next_green)

                    next_pixels.append(next_pixel)

        self.pixels = next_pixels

        return self.pixels
