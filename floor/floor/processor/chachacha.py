import collections
import itertools
from builtins import range

from floor.processor.base import Base, RenderContext
from floor.processor.utils import clocked
from floor.util.color_utils import get_palette

PALLETS = [
    get_palette("rygw"),
    get_palette("unicorns"),
    get_palette("desert"),
]

BLACK = (0, 0, 0)


class ChaChaCha(Base):
    """Chasing boxes."""

    def __init__(self, **kwargs):
        super(ChaChaCha, self).__init__(**kwargs)
        self.pallet = None
        self.lines = None
        self.set_pallet(PALLETS[0])

    def set_pallet(self, pallet):
        if pallet == self.pallet:
            return
        self.pallet = pallet

        lines = []
        for color in self.pallet:
            for i in range(2):
                lines.append([color, color, BLACK, BLACK, color, color, BLACK, BLACK])
                lines.append([color, color, BLACK, BLACK, color, color, BLACK, BLACK])
                lines.append([BLACK, BLACK, color, color, BLACK, BLACK, color, color])
                lines.append([BLACK, BLACK, color, color, BLACK, BLACK, color, color])
        self.lines = collections.deque(lines)

    def on_ranged_value_change(self, num, value):
        if num == RenderContext.RangedInput.WET_DRY:
            pallet = RenderContext.ranged_selection(value, PALLETS)
            self.set_pallet(pallet)

    @clocked(frames_per_beat=2)
    def get_next_frame(self, context):
        lines = list(itertools.islice(self.lines, 0, 8))
        self.lines.rotate()
        pixels = [pixel for line in lines for pixel in line]
        return pixels
