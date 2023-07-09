from __future__ import absolute_import, division, print_function, unicode_literals

from unittest import TestCase

from floor.processor.constants import BLACK, COLOR_MAXIMUM, WHITE

from . import color_utils


class ColorUtilsTests(TestCase):
    def test_normalize_pixel(self):
        self.assertEqual((0, 0, 0, 1.0), color_utils.normalize_pixel((0, 1e-14, 0.000001)))
        self.assertEqual((0, 12, 340, 1.0), color_utils.normalize_pixel((1e-14, 12, 340)))
        self.assertEqual((0, 1023, 340, 1.0), color_utils.normalize_pixel((1e-14, 99999, 340)))
        self.assertEqual((0, 12, 340, 0.5), color_utils.normalize_pixel((1e-14, 12, 340, 0.5)))

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

        # Test `black_is_alpha` function
        above = 0, 0, 1, 1.0
        below = 1, 2, 3
        self.assertEqual((0, 0, 1, 1.0), color_utils.alpha_blend(above, below, 1.0))

        above = 0, 0, 0, 1.0
        self.assertEqual((1, 2, 3), color_utils.alpha_blend(above, below, 1.0))

    def test_tint(self):
        red = (COLOR_MAXIMUM, 0, 0)
        self.assertEqual(red, color_utils.tint(red, 0))
        self.assertEqual(WHITE, color_utils.tint(red, 1))
        self.assertEqual(
            (COLOR_MAXIMUM, COLOR_MAXIMUM // 2, COLOR_MAXIMUM // 2), color_utils.tint(red, 0.5)
        )

    def test_shade(self):
        red = (COLOR_MAXIMUM, 0, 0)
        self.assertEqual(red, color_utils.shade(red, 0))
        self.assertEqual(BLACK, color_utils.shade(red, 1))
        self.assertEqual((511, 0, 0), color_utils.shade(red, 0.5))

    def test_hex_to_rgb(self):
        self.assertEqual(WHITE, color_utils.hex_to_rgb("#ffffff"))
        self.assertEqual(BLACK, color_utils.hex_to_rgb("#000000"))
        self.assertEqual((0, COLOR_MAXIMUM, 0), color_utils.hex_to_rgb("#00ff00"))

    def test_get_pallet(self):
        for p in color_utils.palettes.keys():
            color_utils.get_palette(p)
