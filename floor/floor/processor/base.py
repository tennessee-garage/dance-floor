from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import colorsys


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

class RenderContext:
    """An object that a `Controller` will pass to `Processor.get_next_frame`.

    This class is how the `Controller` passes state to the `Processor`. As such,
    it can be considered write-only for the Controller, and read-only for the Processor.
    """
    def __init__(self, clock, downbeat, weights, bpm):
        self.clock = clock
        self.downbeat = downbeat
        self.weights = weights
        self.bpm = bpm


class Base(object):
    __metaclass__ = ProcessorRegistry

    FLOOR_WIDTH = 8
    FLOOR_HEIGHT = 8
    PIXELS_ALL_OFF = [[0 for _ in range(3)] for _ in range(64)]

    def __init__(self, **kwargs):
        self.weights = []
        self.bpm = None
        self.downbeat = None
        # noinspection PyTypeChecker
        self.controller = kwargs['controller']

    def max_value(self):
        return self.controller.max_led_value()

    # accept (x,y) tuple reflecting a coordinate
    # return the array index suitable for use in weights or pixels arrays
    def idx(self, pixel):
        (x, y) = pixel
        return (x * self.FLOOR_WIDTH) + y

    def get_next_frame(self, context):
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

    def hsv_to_rgb(self, p):
        """Convert a pixel tuple of [h, s, v] to a tuple of [r, g, b]

        HSV values are assumed to range from 0.0 to 1.0
        RGB values are adjusted to range from 0 to self.max_value
        """
        return [int(v * self.max_value) for v in colorsys.hsv_to_rgb(p[0], p[1], p[2])]

    def hsv_to_rgb_pixels(self, pixels):
        """Convert an array of HSV pixels to an array of RGB pixels"""
        return [self.hsv_to_rgb(p) for p in pixels]

    @staticmethod
    def zeroed_pixel_array():
        return [[0, 0, 0] for _ in range(64)]
