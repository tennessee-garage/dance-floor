from __future__ import absolute_import, division, print_function, unicode_literals

import colorsys
import logging
import sys
from builtins import object, range

from floor.processor.constants import COLOR_MAXIMUM, RANGED_INPUT_MAX


class ProcessorRegistry(type):
    """Python metaclass which automatically adds the class to `ALL_PROCESSORS`."""

    ALL_PROCESSORS = {}

    def __new__(cls, clsname, bases, attrs):
        new_class = super(ProcessorRegistry, cls).__new__(cls, clsname, bases, attrs)
        class_name = new_class.__name__
        if class_name != "Base":
            if class_name in cls.ALL_PROCESSORS:
                existing_class = cls.ALL_PROCESSORS[class_name]
                file1 = sys.modules[existing_class.__module__].__file__
                file2 = sys.modules[new_class.__module__].__file__
                files = ", ".join((file1, file2))
                raise ValueError(
                    'Multiple processors with name "{}" declared: {}'.format(class_name, files)
                )
            cls.ALL_PROCESSORS[class_name] = new_class
        return new_class


class RenderContext(object):
    """An object that a `Controller` will pass to `Processor.get_next_frame`.

    This class is how the `Controller` passes state to the `Processor`. As such,
    it can be considered write-only for the Controller, and read-only for the Processor.
    """

    class RangedInput:
        """Simple enum for logical `ranged_values` names."""

        WET_DRY = 0
        INTENSITY = 1
        AUX1 = 2
        AUX2 = 3

    def __init__(self, clock, downbeat, weights, bpm, ranged_values, switches):
        self.clock = clock
        self.downbeat = downbeat
        self.weights = weights
        self.bpm = bpm
        self.ranged_values = ranged_values
        self.switches = switches

    @classmethod
    def ranged_selection(cls, ranged_value, choices):
        """
        Helper method to easily map a set of options to a ranged input.

        Given a list of `choices`, pick the choice matching the current state of
        the ranged_value defined by `input_number`.

        Since ranged inputs have a range of `RANGED_INPUT_MAX` steps, we attempt
        to distribute choices evenly over the range. For example, given choices:

            ['purple', 'yellow', 'orange']

        Then the following values would be returned

            ranged_input  result
            ------------  ------
            0  - 41       purple
            42 - 81       yellow
            82 - 127      orange

        When the number of choices cannot be evenly divided by the number of steps
        in the range, the final choice receives the balance. This is illustrated above,
        since `128 // 3 == 42`, but `42 * 3 < 127`.
        """
        choices = choices[: RANGED_INPUT_MAX + 1]
        num_choices = len(choices)
        steps_per_choice = (RANGED_INPUT_MAX + 1) // num_choices
        current_position = ranged_value
        return choices[min(num_choices - 1, current_position // steps_per_choice)]


class Base(metaclass=ProcessorRegistry):
    CONTROLS = []

    FLOOR_WIDTH = 8
    FLOOR_HEIGHT = 8
    PIXELS_ALL_OFF = [[0 for _ in range(3)] for _ in range(64)]

    def __init__(self, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.weights = []
        self.ranged_values = []

        self._controls = []
        self.init_controls()

    def init_controls(self):
        for item in self.CONTROLS:
            name = item["name"]
            if name in self.__dict__:
                raise AttributeError(
                    "Proposed control name {} already exists in class".format(name)
                )

            if "range" in item:
                self.add_range_control(name, item)
            elif "scale" in item:
                self.add_scale_control(name, item)
            else:
                self.add_absolute_control(name, item)

    def add_absolute_control(self, name, item):
        if "default" in item:
            default = item["default"]
        else:
            default = 0

        self._controls.append({"name": name, "handler": lambda input_value: input_value})
        self.__dict__[name] = default

    def add_scale_control(self, name, item):
        scale = item["scale"]
        item["range"] = [0.0, scale]
        return self.add_range_control(name, item)

    def add_range_control(self, name, item):
        r = item["range"]
        handler = self.get_range_handler(0, 127, r[0], r[1])

        if "default" in item:
            default = item["default"]
        else:
            default = r[0]

        self._controls.append({"name": name, "handler": handler})
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

    def get_next_frame(self, context):
        """
        Generate the LED values needed for the next frame
        :return:
        """
        pass

    def on_ranged_value_change(self, num, val):
        if num >= len(self._controls):
            return

        control = self._controls[num]
        name = control["name"]
        handler = control["handler"]
        output_value = handler(val)
        self.__dict__[name] = output_value
        self.logger.info("Set control {} to {}".format(name, output_value))

    def hsv_to_rgb(self, p):
        """Convert a pixel tuple of [h, s, v] to a tuple of [r, g, b]

        HSV values are assumed to range from 0.0 to 1.0
        RGB values are adjusted to range from 0 to COLOR_MAXIMUM
        """
        return [int(v * COLOR_MAXIMUM) for v in colorsys.hsv_to_rgb(p[0], p[1], p[2])]

    def hsv_to_rgb_pixels(self, pixels):
        """Convert an array of HSV pixels to an array of RGB pixels"""
        return [self.hsv_to_rgb(p) for p in pixels]

    @staticmethod
    def zeroed_pixel_array():
        return [[0, 0, 0] for _ in range(64)]
