from __future__ import absolute_import, division, print_function, unicode_literals

import os
from unittest import TestCase

from mock import Mock

from floor.controller.controller import Controller
from floor.controller.playlist import Playlist, PlaylistManager
from floor.processor import all_processors
from floor.processor.base import Base as BaseProcessor

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_PLAYLIST = BASE_DIR + "/../../config/playlists/default.json"


RED = (0xFF, 0x00, 0x00)
GREEN = (0x00, 0xFF, 0x00)
BLUE = (0x00, 0x00, 0xFF)
BLACK = (0x00, 0x00, 0x00)


class SingleColorProcessor(BaseProcessor):
    """A test processor that sets all pixels to a single color."""

    def __init__(self, **kwargs):
        self.color = kwargs.pop("color", BLACK)
        super(SingleColorProcessor, self).__init__(**kwargs)

    def get_next_frame(self, context):
        return [self.color] * 64


class ControllerTest(TestCase):
    @staticmethod
    def new_fake_driver():
        driver = Mock()
        driver.get_weights = Mock(return_value=[0] * 64)
        return driver

    def setUp(self):
        all_procs = all_processors()
        self.playlist = Playlist.from_file(DEFAULT_PLAYLIST, all_procs)
        self.playlist_manager = PlaylistManager(self.playlist)
        self.driver = Mock()
        self.driver = self.new_fake_driver()
        self.controller = Controller([self.driver], self.playlist_manager)

    def test_initialization(self):
        """Verifies initial state."""
        c = self.controller
        self.assertEqual(120, c.bpm)
        self.assertEqual(120, c.fps)

    def test_rendering(self):
        c = self.controller
        c.run_one_frame()
        self.driver.set_leds.assert_called_once()
        self.driver.get_weights.assert_called_once()
        self.driver.read_data.assert_called_once()
        self.driver.send_data.assert_called_once()

        first_processor_class = self.playlist.queue[0].processor_cls
        self.assertEqual(first_processor_class, c.layers["playlist"].current_processor.__class__)

    def test_layer_blending(self):
        red_processor = SingleColorProcessor(color=RED)
        green_processor = SingleColorProcessor(color=GREEN)

        playlist = Playlist.from_single_processor(SingleColorProcessor, args={"color": BLUE})
        playlist_manager = PlaylistManager(playlist)
        driver = self.new_fake_driver()
        controller = Controller([driver], playlist_manager)

        controller.run_one_frame()
        self.assertEqual([BLUE + (1.0,)] * 64, driver.set_leds.call_args[0][0])

        overlay2 = controller.layers["overlay2"]
        overlay2.set_processor(red_processor)
        overlay2.set_alpha(0.5)
        controller.run_one_frame()
        self.assertEqual([(0x7F, 0x00, 0x7F)] * 64, driver.set_leds.call_args[0][0])

        overlay1 = controller.layers["overlay1"]
        overlay1.set_processor(green_processor)
        overlay1.set_alpha(0.5)
        controller.run_one_frame()
        self.assertEqual([(0x3F, 0x7F, 0x3F)] * 64, driver.set_leds.call_args[0][0])

    def test_multiple_drivers_get_weights_are_blended(self):
        driver1 = Mock()
        driver1.get_weights = Mock(return_value=[0, 1, 0, 0] * 16)

        driver2 = Mock()
        driver2.get_weights = Mock(return_value=[0, 0, 0, 1] * 16)

        playlist = Playlist.from_file(DEFAULT_PLAYLIST, all_processors())
        playlist_manager = PlaylistManager(playlist)
        controller = Controller([driver1, driver2], playlist_manager)
        weights = controller.get_weights()

        expected_weights = [0, 1] * 32
        self.assertEqual(expected_weights, weights)

        controller.square_weight_on(1)
        expected_weights[0] = 1
        weights = controller.get_weights()
        self.assertEqual(expected_weights, weights)

        controller.square_weight_off(1)
        expected_weights[0] = 0
        weights = controller.get_weights()
        self.assertEqual(expected_weights, weights)
