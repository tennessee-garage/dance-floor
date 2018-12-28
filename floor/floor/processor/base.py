from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging


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

    CONTROLS = []

    DEFAULT_MAX_VALUE = 1024
    FLOOR_WIDTH = 8
    FLOOR_HEIGHT = 8
    PIXELS_ALL_OFF = [[0 for _ in range(3)] for _ in range(64)]

    def __init__(self, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.weights = []
        self.max_value = self.DEFAULT_MAX_VALUE
        self.bpm = None
        self.downbeat = None
        self.ranged_values = []

        self._controls = []
        self.init_controls()

    def init_controls(self):
        for item in self.CONTROLS:
            name = item['name']
            if name in self.__dict__:
                raise AttributeError('Proposed control name {} already exists in class'.format(name))

            if 'range' in item:
                self.add_range_control(name, item)
            elif 'scale' in item:
                self.add_scale_control(name, item)
            else:
                self.add_absolute_control(name, item)

    def add_absolute_control(self, name, item):
        if 'default' in item:
            default = item['default']
        else:
            default = 0

        self._controls.append({
            'name': name,
            'handler': lambda input_value: input_value
        })
        self.__dict__[name] = default

    def add_scale_control(self, name, item):
        scale = item['scale']
        item['range'] = [0.0, scale]
        return self.add_range_control(name, item)

    def add_range_control(self, name, item):
        r = item['range']
        handler = self.get_range_handler(0, 127, r[0], r[1])

        if 'default' in item:
            default = item['default']
        else:
            default = r[0]

        self._controls.append({
            'name': name,
            'handler': handler
        })
        self.__dict__[name] = default

    @classmethod
    def get_range_handler(cls, input_min, input_max, output_min, output_max):
        input_delta = input_max - input_min
        output_delta = output_max - output_min

        def range_handler(input_value):
            return output_min + (float(input_value - input_min) / input_delta) * output_delta

        return range_handler

    # accept (x,y) tuple reflecting a coordinate
    # return the array index suitable for use in weights or pixels arrays
    def idx(self, pixel):
        (x, y) = pixel
        return (x * self.FLOOR_WIDTH) + y

    def set_max_value(self, max_value):
        self.max_value = max_value

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

    def on_ranged_value_change(self, num, val):
        if num >= len(self._controls):
            return

        control = self._controls[num]
        name = control['name']
        handler = control['handler']
        output_value = handler(val)
        self.__dict__[name] = output_value
        self.logger.info("Set control {} to {}".format(name, output_value))
