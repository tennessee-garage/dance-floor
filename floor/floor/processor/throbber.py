from builtins import range

from floor.processor.base import Base
from floor.util.color_utils import hex_to_rgb

RED = hex_to_rgb("#ff0000")
YELLOW = hex_to_rgb("#ffff00")
GREEN = hex_to_rgb("#00ff00")
BLUE = hex_to_rgb("#0000ff")

COLORS = [RED, YELLOW, GREEN, BLUE]


def draw_line(arr, start, end, pixel):
    for x in range(start[0], end[0] + 1):
        for y in range(start[1], end[1] + 1):
            arr[x + y * 8] = pixel


class Throbber(Base):
    """Shows an outward moving square according to bpm."""

    def get_next_frame(self, context):
        now = context.clock
        downbeat = context.downbeat or now

        seconds_per_measure = (1 / (context.bpm / 60.0)) * 4
        position_in_measure = (now - downbeat) % seconds_per_measure
        beat_in_measure = int(position_in_measure / seconds_per_measure * 4)

        seconds_per_phrase = seconds_per_measure * 4
        position_in_phrase = (now - downbeat) % seconds_per_phrase
        measure_in_phrase = int(position_in_phrase / seconds_per_phrase * 4)

        pixels = [(0, 0, 0)] * 64
        color = COLORS[measure_in_phrase]

        if beat_in_measure == 0:
            draw_line(pixels, (3, 3), (3, 4), color)
            draw_line(pixels, (4, 3), (4, 4), color)
        elif beat_in_measure == 1:
            draw_line(pixels, (2, 2), (2, 5), color)
            draw_line(pixels, (5, 2), (5, 5), color)
            draw_line(pixels, (2, 2), (5, 2), color)
            draw_line(pixels, (2, 5), (5, 5), color)
        elif beat_in_measure == 2:
            draw_line(pixels, (1, 1), (1, 6), color)
            draw_line(pixels, (6, 1), (6, 6), color)
            draw_line(pixels, (1, 1), (6, 1), color)
            draw_line(pixels, (1, 6), (6, 6), color)
        else:
            draw_line(pixels, (0, 0), (0, 7), color)
            draw_line(pixels, (7, 0), (7, 7), color)
            draw_line(pixels, (0, 0), (7, 0), color)
            draw_line(pixels, (0, 7), (7, 7), color)

        return pixels
