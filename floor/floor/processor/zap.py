import collections

from base import Base
from utils import clocked


def tint(color, percent):
    """Lighten `color` to white by `percent`"""
    r, g, b = color
    new_r = r + (255 - r) * percent
    new_g = g + (255 - g) * percent
    new_b = b + (255 - b) * percent
    return new_r, new_g, new_b


def gradient(color, steps=4):
    """Fade this color to white."""
    ret = []
    denominator = float(steps - 1)
    for step in xrange(steps):
        percent = step / denominator
        ret.append(tint(color, percent))
    return ret


RED = (0xff, 0x00, 0x00)
ORANGE = (0xff, 0xa5, 0x00)
GREEN = (0x00, 0xff, 0x00)
YELLOW = (0xff, 0xff, 0x00)
BLUE = (0, 0, 0xff)
PURPLE = (0x94, 0x00, 0xd3)

COLOR_SETS = [
    gradient(RED),
    gradient(ORANGE),
    gradient(YELLOW),
    gradient(GREEN),
    gradient(BLUE),
    gradient(PURPLE),
]

FRAMES = [
    [(0, 0, 0)] * 64,
    [(0, 0, 0)] * 64,
    [(0, 0, 0)] * 64,
    [(0, 0, 0)] * 64,
]


def draw_line(arr, start, end, pixel):
    for x in range(start[0], end[0] + 1):
        for y in range(start[1], end[1] + 1):
            arr[x + y * 8] = pixel


# Pre-render all frames. `FRAME_SETS` is a list-of-lists; each item
# in FRAME_SETS is a frameset of 4 frames for a particular color.
#
# The processor selects a new frameset every 4th beat, and a new
# frame from the current frameset every beat.
FRAME_SETS = []
for color_set in COLOR_SETS:
    frame_set = [
        [(0, 0, 0)] * 64,
        [(0, 0, 0)] * 64,
        [(0, 0, 0)] * 64,
        [(0, 0, 0)] * 64,
    ]

    draw_line(frame_set[3], (3, 3), (3, 4), color_set[3])
    draw_line(frame_set[3], (4, 3), (4, 4), color_set[3])

    draw_line(frame_set[2], (2, 2), (2, 5), color_set[2])
    draw_line(frame_set[2], (5, 2), (5, 5), color_set[2])
    draw_line(frame_set[2], (2, 2), (5, 2), color_set[2])
    draw_line(frame_set[2], (2, 5), (5, 5), color_set[2])

    draw_line(frame_set[1], (1, 1), (1, 6), color_set[1])
    draw_line(frame_set[1], (6, 1), (6, 6), color_set[1])
    draw_line(frame_set[1], (1, 1), (6, 1), color_set[1])
    draw_line(frame_set[1], (1, 6), (6, 6), color_set[1])

    draw_line(frame_set[0], (0, 0), (0, 7), color_set[0])
    draw_line(frame_set[0], (7, 0), (7, 7), color_set[0])
    draw_line(frame_set[0], (0, 0), (7, 0), color_set[0])
    draw_line(frame_set[0], (0, 7), (7, 7), color_set[0])
    FRAME_SETS.append(frame_set)


class Zap(Base):
    """Chasing boxes."""

    def __init__(self, **kwargs):
        super(Zap, self).__init__(**kwargs)
        self.frame_sets = collections.deque(FRAME_SETS)
        self.frames = collections.deque(self.frame_sets[0])
        self.last_downbeat = None
        self.beat_counter = 0

    def change_color_if_needed(self):
        if self.last_downbeat is None:
            self.last_downbeat = self.downbeat
        elif self.downbeat != self.last_downbeat:
            self.beat_counter = 0
            self.last_downbeat = self.downbeat

        if self.beat_counter % 4 == 0:
            self.frame_sets.rotate(n=1)
            self.frames = collections.deque(self.frame_sets[0])

        self.beat_counter += 1

    @clocked(frames_per_beat=1)
    def get_next_frame(self, weights):
        self.change_color_if_needed()
        frame = self.frames[0]
        self.frames.rotate(-1)
        return frame
