from base import Base
import random
from random import randint

import time
import math

life_time = 4

def create():
    return LandMines()


class LandMines(Base):
    def __init__(self):
        super(LandMines, self).__init__()
        self.pixels = []
        self.mines = []
        self.walkers = self.init_walkers()
        for x in range(0, 8):
            for y in range(0, 8):
                self.pixels.append((0, 0, 0))

    def init_walkers(self):
        walkers = []
        walkers.append({'x':0, 'y':0})
        walkers.append({'x':0, 'y':7})
        walkers.append({'x':7, 'y':0})
        walkers.append({'x':7, 'y':7})
        return walkers

    def get_walker(self):
        walker = self.walkers[randint(0, 2)]
        #take a random step
        walker['x'] += randint(-1, 1)
        if walker['x']<0:
            walker['x'] = 0
        if walker['x']>7:
            walker['x'] = 7
        walker['y'] += randint(-1, 1)
        if walker['y']<0:
            walker['y'] = 0
        if walker['y']>7:
            walker['y'] = 7
        return walker

    def build_mine(self, x, y):
        t = life_time
        color = [0,0,0]
        color[0] = randint(0, 1)*self.max_value
        color[1] = randint(0, 1)*self.max_value
        color[2] = randint(0, 1)*self.max_value
        color = tuple(color)
        return {'x':x, 'y':y, 't':t, 'color':color}


    # For each mine in mines:
    # 1. If delta_time < life_time/2 Increment by: velocity * delta_time / radius
    # 2. If delta_time > life_time/2 Decrement by: velocity * delta_time / radius
    # 3. If delta_time > life_time, remove mine
    def get_next_frame(self, weights):
        next_time = time.time()

        chance = random.random()
        if chance > 0.9:
            walker = self.get_walker()
            x = walker['x']
            y = walker['y']
            mine = self.build_mine(x, y)
            self.mines.append(mine)
            self.pixels[mine['y']*8 + mine['x']] = mine['color']

        time_delta = 0.1
        velocity = 0.0003 * self.max_value
        live_mines = []
        for index in xrange(len(self.mines)):
            mine = self.mines[index]
            mine['t'] -= time_delta
            delta_time = life_time - mine['t']
            color = mine['color']
            toggle = 1

            #when the mine hits half a life_time, reverse the explosion
            if mine['t'] < life_time/2:
                toggle = -1

            #if the mine has time left, compute explosion, store it in live_mines for next time
            if mine['t'] > 0.0:
                live_mines.append(mine)
                for y in range(0, 8):
                    for x in range(0, 8):
                        next_pixel = self.pixels[y*8 + x]
                        radius = math.sqrt((x-mine['x'])*(x-mine['x']) + (y-mine['y'])*(y-mine['y']))

                        #don't divide by zero :)
                        if radius>0:
                            delta = toggle * velocity * delta_time / radius
                            next_red = next_pixel[0] + delta*color[0]
                            next_blue = next_pixel[1] + delta*color[1]
                            next_green = next_pixel[2] + delta*color[2]
                            # don't let values go negative
                            if next_blue<0:
                                next_blue = 0
                            if next_red<0:
                                next_red = 0
                            if next_green<0:
                                next_green = 0
                            self.pixels[y*8 + x] = (next_red, next_blue, next_green)

            #if the mine doesn't have time left, 0 it out and don't add it to live_mines
            else:
                self.pixels[mine['y']*8 + mine['x']] = (0,0,0)

        self.mines = live_mines

        return self.pixels
