

class Base(object):

    DEFAULT_MAX_VALUE = 1024
    FLOOR_WIDTH = 8
    FLOOR_HEIGHT = 8

    def __init__(self, **kwargs):
        self.weights = []
        self.max_value = self.DEFAULT_MAX_VALUE
        self.bpm = None
        self.downbeat = None

    # accept (x,y) tuple reflecting a coordinate
    # return the array index suitable for use in weights or pixels arrays
    def idx(self, pixel):
        (x, y) = pixel
        return (x * self.FLOOR_WIDTH) + y

    def set_max_value(self, max_value):
        self.max_value = max_value

    def get_next_frame(self, weights):
        """
        Generate the LED values needed for the next frame
        :return:
        """
        pass

    def requested_fps(self):
        """
        If this processor wants a specific FPS, it can override this method
        :return: integer - a number giving the Frames per Second to run this processor at
        """
        return None

    def set_bpm(self, bpm, downbeat):
        """
        Sets the current BPM and the time of the downbeat.

        Args
            bpm: float number of beats per minute
            downbeat: timestamp corresponding to the first beat of a new
                measure.
        """
        assert downbeat is not None
        self.bpm = bpm
        self.downbeat = downbeat
