import collections
import itertools

from base import Base
from utils import clocked

BLACK = (0, 0, 0)
RED = (0xff, 0x00, 0x00)
YELLOW = (0xff, 0xf0, 0x00)
GREEN = (0x00, 0xff, 0x00)
WHITE = (0xff, 0xff, 0xff)

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
        self.lines.rotate(n=1)
        pixels = [pixel for line in lines for pixel in line]
        return pixels
