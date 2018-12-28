from spiral import Spiral
from utils import clocked


class SpiralBeat(Spiral):

    @clocked(frames_per_beat=1)
    def get_next_frame(self, weights):
        super(SpiralBeat, self).get_next_frame(weights)
