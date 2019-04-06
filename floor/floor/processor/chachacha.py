from builtins import range
import collections
import itertools

from floor.processor.base import Base
from floor.processor.utils import clocked
from floor.processor.constants import COLOR_MAXIMUM

BLACK = (0, 0, 0)
RED = (1, 0, 0)
YELLOW = (1, 0xf0/float(0xff), 0)
GREEN = (0, 1, 0)
WHITE = (1, 1, 1)

COLORS = [RED, YELLOW, GREEN, WHITE]

# Pre-render the boxes.
LINES = []
for color in COLORS:
    for i in range(2):
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
    def get_next_frame(self, context):
        lines = list(itertools.islice(self.lines, 0, 8))
        self.lines.rotate()
        pixels = [(pixel[0] * COLOR_MAXIMUM, pixel[1] * COLOR_MAXIMUM, pixel[2] * COLOR_MAXIMUM)
                  for line in lines for pixel in line]
        return pixels
