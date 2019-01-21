from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from floor.processor import all_processors
from floor.controller.controller import Controller
from floor.controller.playlist import Playlist
from unittest import TestCase
from mock import Mock


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_PLAYLIST = BASE_DIR + '/../../config/playlists/default.json'


class ControllerTest(TestCase):
    def setUp(self):
        self.playlist = Playlist.from_file(all_processors(), DEFAULT_PLAYLIST)
        self.driver = Mock()
        self.driver.get_max_led_value = Mock(return_value=1022)
        self.controller = Controller(self.driver, self.playlist)

    def test_initialization(self):
        """Verifies initial state."""
        c = self.controller
        self.assertEqual(120, c.bpm)
        self.assertEqual(24, c.fps)
        self.assertEqual(1022, c.max_led_value)
        self.assertEqual(1022, c.max_effective_led_value)

    def test_rendering(self):
        c = self.controller
        c.run_one_frame()
        self.driver.set_leds.assert_called_once()
        self.driver.get_weights.assert_called_once()
        self.driver.read_data.assert_called_once()
        self.driver.send_data.assert_called_once()

        first_processor_name = self.playlist.queue[0]['name']
        self.assertEqual(first_processor_name, c.processor.__class__.__name__)

        
