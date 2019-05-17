from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from unittest import TestCase
from . import color_utils


class ColorUtilsTests(TestCase):
    def test_normalize_pixel(self):
        self.assertEqual((0, 0, 0), color_utils.normalize_pixel((0, 1e-14, 0.000001)))
        self.assertEqual((0, 12, 340), color_utils.normalize_pixel((1e-14, 12, 340)))
        self.assertEqual((0, 1024, 340), color_utils.normalize_pixel((1e-14, 99999, 340)))

    def test_alpha_blend(self):
        above = 255, 255, 255
        below = 0, 0, 0

        self.assertEqual((255, 255, 255), color_utils.alpha_blend(above, below, 1.0))
        self.assertEqual((127, 127, 127), color_utils.alpha_blend(above, below, 0.50))

        above = 255, 0, 0
        self.assertEqual((63, 0, 0), color_utils.alpha_blend(above, below, 0.25))

        above = 0, 255, 0
        self.assertEqual((0, 63, 0), color_utils.alpha_blend(above, below, 0.25))

        above = 0, 0, 255
        self.assertEqual((0, 0, 63), color_utils.alpha_blend(above, below, 0.25))
