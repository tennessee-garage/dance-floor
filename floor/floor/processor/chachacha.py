import collections
import itertools

from base import Base
from utils import clocked

BLACK = (0, 0, 0)
RED = (1, 0, 0)
YELLOW = (1, 0xf0/float(0xff), 0)
GREEN = (0, 1, 0)
WHITE = (1, 1, 1)

COLORS = [RED, YELLOW, GREEN, WHITE]

# Pre-render the boxes.
LINES = []
for color in COLORS:
    for i in xrange(2):
        LINES.append([color, color, BLACK, BLACK, color, color, BLACK, BLACK])
        LINES.append([color, color, BLACK, BLACK, color, color, BLACK, BLACK])
        LINES.append([BLACK, BLACK, color, color, BLACK, BLACK, color, color])
        LINES.append([BLACK, BLACK, color, color, BLACK, BLACK, color, color])


class ChaChaCha(Base):
    """Chasing boxes."""

    def __init__(self, **kwargs):
        super(ChaChaCha, self).__init__(**kwargs)
        self.lines = collections.deque(LINES)

    @clocked(frames_per_beat=2)
    def get_next_frame(self, weights):
        lines = list(itertools.islice(self.lines, 0, 8))
        self.lines.rotate()
        pixels = [(pixel[0] * self.max_value, pixel[1] * self.max_value, pixel[2] * self.max_value)
                  for line in lines for pixel in line]
        return pixels