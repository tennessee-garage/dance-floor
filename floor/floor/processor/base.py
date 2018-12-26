from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class ProcessorRegistry(type):
    """Python metaclass which automatically adds the class to `ALL_PROCESSORS`."""
    ALL_PROCESSORS = {}

    def __new__(cls, clsname, bases, attrs):
        new_class = super(ProcessorRegistry, cls).__new__(cls, clsname, bases, attrs)
        class_name = new_class.__name__
        if class_name in cls.ALL_PROCESSORS:
            raise ValueError('Multiple processors with name "{}" declared'.format(class_name))
        cls.ALL_PROCESSORS[class_name] = new_class
        return new_class


class Base(object):
    __metaclass__ = ProcessorRegistry

    DEFAULT_MAX_VALUE = 1024
    FLOOR_WIDTH = 8
    FLOOR_HEIGHT = 8
    PIXELS_ALL_OFF = [[0 for _ in range(3)] for _ in range(64)]

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

    @staticmethod
    def zeroed_pixel_array():
        return [[0, 0, 0] for _ in range(64)]
