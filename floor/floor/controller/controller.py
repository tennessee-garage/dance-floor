from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import time
from builtins import object, range
from collections import OrderedDict

from floor import processor
from floor.controller.playlist import PlaylistManager
from floor.controller.rendering import PlaylistRenderLayer, ProcessorRenderLayer
from floor.processor.base import RenderContext
from floor.util.color_utils import alpha_blend, normalize_pixel, set_brightness
from floor.util.simple_profile import profile

logger = logging.getLogger("controller")


class Controller(object):
    DEFAULT_FPS = 120
    DEFAULT_BPM = 120.0

    def __init__(self, drivers, playlist_manager, clocksource=time):
        """Constructor.

        Arguments:
            drivers {floor.driver.Base} -- One or more drivers for show output
            playlist_manager {floor.playlist.PlaylistManager} -- The show's playlist manager

        Keyword Arguments:
            clocksource {function} -- An object that should have `.time()`
            and `.sleep()` methods (default: {time})
        """
        assert len(drivers) > 0, "Must provide 1 or more drivers"
        self.drivers = drivers
        assert isinstance(
            playlist_manager, PlaylistManager
        ), "playlist_manager is not a PlaylistManager"
        self.playlist_manager = playlist_manager
        self.clocksource = clocksource
        self.frame_start = 0
        self.fps = None
        self.frame_seconds = None

        self.all_processors = processor.all_processors()

        self.set_fps(self.DEFAULT_FPS)

        # Ordered dict of layers to render, bottom-most layer first.
        self.layers = OrderedDict(
            (
                (
                    "playlist",
                    PlaylistRenderLayer(
                        playlist_manager=self.playlist_manager, all_processors=self.all_processors
                    ),
                ),
                ("overlay2", ProcessorRenderLayer()),
                ("overlay1", ProcessorRenderLayer()),
            )
        )

        self.bpm = None
        self.downbeat = None
        self.set_bpm(self.DEFAULT_BPM)

        # Give outside controllers a chance to fake foot steps on the floor
        self.synthetic_weights = [0] * 64

        # A global "brightness" level, a value between 0.0 and 1.0.
        self.brightness = 1.0

    def _iter_enabled_layers(self):
        """Returns an iterable of all enabled layers."""
        return [layer for layer in list(self.layers.values()) if layer.is_enabled()]

    def set_fps(self, fps):
        self.fps = fps
        self.frame_seconds = 1.0 / fps

    def set_bpm(self, bpm, downbeat=None):
        logger.info("Setting bpm to: {}".format(bpm))
        self.bpm = float(bpm)
        self.downbeat = downbeat or self.clocksource.time()

    def set_brightness(self, factor):
        """Scale the default brightness from 0 to max for driver

        :param factor: a scaling factor from 0.0 to 1.0
        :return: none
        """
        self.brightness = max(0.0, min(1.0, factor))
        logger.info("Set brightness to: {}%".format(int(self.brightness * 100)))

    def handle_input_event(self, event_name, num, value):
        logger.debug("input event: {}: {} -> {}".format(event_name, num, value))
        if event_name == "playlist_ranged_value":
            self.layers["playlist"].on_ranged_value_change(num, value)
        elif event_name == "overlay1_ranged_value":
            self.layers["overlay1"].on_ranged_value_change(num, value)
        elif event_name == "overlay2_ranged_value":
            self.layers["overlay2"].on_ranged_value_change(num, value)
        elif event_name == "playlist_switch":
            self.layers["playlist"].on_switch_change(num, value)
        elif event_name == "overlay1_switch":
            self.layers["overlay1"].on_switch_change(num, value)
        elif event_name == "overlay2_switch":
            self.layers["overlay2"].on_switch_change(num, value)
        else:
            logger.warning("Ignoring unknown event {}".format(event_name))

    def square_weight_on(self, index):
        if index > 64 or index < 1:
            logger.error("Ignoring square_weight_on() value beyond bounds")
            return
        self.synthetic_weights[index - 1] = 1

    def square_weight_off(self, index):
        if index > 64 or index < 1:
            logger.error("Ignoring square_weight_on() value beyond bounds")
            return
        self.synthetic_weights[index - 1] = 0

    def run_forever(self):
        while True:
            self.run_one_frame()

    @profile(print_seconds=2)
    def run_one_frame(self):
        self.init_loop()
        self.generate_frame()
        self.transfer_data()
        self.delay()

    @profile()
    def init_loop(self):
        self.frame_start = self.clocksource.time()

    @profile()
    def generate_frame(self):
        weights = self.get_weights()
        composited_leds = [(0, 0, 0)] * 64
        for layer in self._iter_enabled_layers():
            context = RenderContext(
                clock=self.frame_start,
                downbeat=self.downbeat,
                weights=weights,
                bpm=self.bpm,
                ranged_values=layer.ranged_values,
                switches=layer.switches,
            )
            current_leds = layer.render(context)
            if not current_leds:
                continue
            for idx, current_pixel in enumerate(current_leds):
                current_pixel = normalize_pixel(current_pixel)
                last_pixel = composited_leds[idx]
                composited_leds[idx] = alpha_blend(current_pixel, last_pixel, layer.get_alpha())

        leds = [set_brightness(pixel, self.brightness) for pixel in composited_leds]
        for driver in self.drivers:
            driver.set_leds(leds)

    @profile()
    def get_weights(self):
        # Returns a single frame of weights, by taking the `max()` of
        # every driver's reported weight for every pixel.
        all_weights = [driver.get_weights() for driver in self.drivers]
        all_weights.append(self.synthetic_weights)

        weights = [0] * 64
        for i in range(len(weights)):
            max_weight = max(w[i] if len(w) > i else 0 for w in all_weights)
            weights[i] = max_weight
        return weights

    @profile()
    def transfer_data(self):
        for driver in self.drivers:
            driver.send_data()
            driver.read_data()

    @profile()
    def delay(self):
        elapsed = self.clocksource.time() - self.frame_start

        if elapsed < self.frame_seconds:
            self.clocksource.sleep(self.frame_seconds - elapsed)
        else:
            logger.debug("Over by {}".format(elapsed - self.frame_seconds))
