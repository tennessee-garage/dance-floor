from base import Base
import time

RED = (0xff, 0x00, 0x00)
YELLOW = (0xff, 0xf0, 0x00)
GREEN = (0x00, 0xff, 0x00)
BLUE = (0x00, 0x00, 0xff)

COLORS = [RED, YELLOW, GREEN, BLUE]

def draw_line(arr, start, end, pixel):
    for x in range(start[0], end[0] + 1):
        for y in range(start[1], end[1] + 1):
            arr[x + y * 8] = pixel

class Throbber(Base):
    """Shows an outward moving square according to bpm."""

    def get_next_frame(self, weights):
        now = time.time()
        downbeat = self.downbeat or now

        seconds_per_measure = (1 / (self.bpm / 60)) * 4
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


def create(args=None):
    return Throbber()
