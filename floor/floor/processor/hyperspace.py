import time
import math

from base import Base
import floor.util.color_utils as color


class Hyperspace(Base):

    LIFETIME = 1.0

    def __init__(self, **kwargs):
        super(Hyperspace, self).__init__(**kwargs)
        self.pixels = []
        self.times = [0 for _ in range(64)]
        # self.palette = color.get_random_palette(self.max_value)
        self.palette = color.get_palette('rainbow_bunny', self.max_value)
        self.palette_length = len(self.palette)
        self.radius_map_1 = [None] * 64
        self.radius_map_2 = [None] * 64
        self.start_time = None

        self.radius_map_1 = self.build_radius_map({'x':3.5, 'y':3.5});
        self.radius_map_2 = self.build_radius_map({'x':3, 'y':4});

    # precompute distance of each pixel to the center
    def build_radius_map(self, center):
        radius_map = [None] * 64
        for y in range(0, self.FLOOR_HEIGHT):
            for x in range(0, self.FLOOR_WIDTH):
                index = self.idx((x, y))
                radius = math.sqrt((x-center['x'])*(x-center['x']) + (y-center['y'])*(y-center['y']))
                radius_map[index] = radius
        return radius_map

    def offset_frame(self, frame, offset):
        new_frame = [None] * 64
        for y in range(0, self.FLOOR_HEIGHT):
            for x in range(0, self.FLOOR_WIDTH):
                index = self.idx((x, y))
                offset_x = int((x - offset['x']) % self.FLOOR_WIDTH)
                offset_y = int((y - offset['y']) % self.FLOOR_HEIGHT)
                offset_index = self.idx((offset_x, offset_y))
                new_frame[index] = frame[offset_index]

        return new_frame

    def next_offset(self, delta):
        time_slice = math.sin(0.1*delta)
        radius = 5
        velocity = 4
        if time_slice < -0.7:
            #move down/right
            offset = {'x':velocity*delta, 'y':velocity*delta}
        elif time_slice < 0.0:
            #orbit
            offset = {'x':radius*math.sin(velocity*delta), 'y':radius*math.cos(velocity*delta)}
        elif time_slice < 0.7:
            #move up/left
            offset = {'x':-1*velocity*delta, 'y':-1*velocity*delta}
        else:
            #stay centered
            offset = {'x':0, 'y':0}

        return offset

    def get_next_frame(self, context):
        if self.start_time is None:
            self.start_time = context.clock
        delta = context.clock - self.start_time
        pulse = 2*math.sin(0.5*delta)
        frame = [None] * 64
        for y in range(0, self.FLOOR_HEIGHT):
            for x in range(0, self.FLOOR_WIDTH):
                index = self.idx((x, y))
                radius = self.radius_map_1[index]
                color = self.palette[int(radius*pulse % self.palette_length)]
                frame[index] = color

        offset = self.next_offset(delta)
        frame = self.offset_frame(frame, offset)

        return frame
