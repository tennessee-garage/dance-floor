from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import range
from builtins import object
import time
import logging
from collections import OrderedDict

from floor import processor
from floor.processor.base import RenderContext
from floor.controller.rendering import PlaylistRenderLayer
from floor.controller.rendering import ProcessorRenderLayer
from floor.util.color_utils import alpha_blend
from floor.util.color_utils import normalize_pixel
from floor.util.color_utils import set_brightness
from floor.util.simple_profile import profile


logger = logging.getLogger('controller')


class Controller(object):
    DEFAULT_FPS = 120
    DEFAULT_BPM = 120.0

    # Give outside controllers a chance to fake foot steps on the floor
    # Use the SYNTHETIC_WEIGHT_ACTIVE flag to determine if we need to spend
    # cycles mixing in the weight values.
    SYNTHETIC_WEIGHT_ACTIVE = False
    SYNTHETIC_WEIGHTS = [0]*64

    def __init__(self, driver, playlist, clocksource=time):
        """Constructor.
        
        Arguments:
            driver {floor.driver.Base} -- The driver powering the show
            playlist {floor.playlist.Playlist} -- The show's playlist
        
        Keyword Arguments:
            clocksource {function} -- An object that should have `.time()`
            and `.sleep()` methods (default: {time})
        """

        self.driver = driver
        self.playlist = playlist
        self.clocksource = clocksource
        self.frame_start = 0
        self.fps = None
        self.frame_seconds = None

        self.all_processors = processor.all_processors()

        self.set_fps(self.DEFAULT_FPS)

        # Ordered dict of layers to render, bottom-most layer first.
        self.layers = OrderedDict((
            ('playlist', PlaylistRenderLayer(playlist=self.playlist, all_processors=self.all_processors)),
            ('overlay2', ProcessorRenderLayer()),
            ('overlay1', ProcessorRenderLayer()),
        ))

        self.bpm = None
        self.downbeat = None
        self.set_bpm(self.DEFAULT_BPM)

        # A global "brightness" level, a value between 0.0 and 1.0.
        self.brightness = 1.0

    def _iter_enabled_layers(self):
        """Returns an iterable of all enabled layers."""
        return [layer for layer in list(self.layers.values()) if layer.is_enabled()]

    def set_fps(self, fps):
        self.fps = fps
        self.frame_seconds = 1.0/fps

    def set_bpm(self, bpm, downbeat=None):
        logger.info('Setting bpm to: {}'.format(bpm))
        self.bpm = float(bpm)
        self.downbeat = downbeat or self.clocksource.time()

    def set_brightness(self, factor):
        """Scale the default brightness from 0 to max for driver

        :param factor: a scaling factor from 0.0 to 1.0
        :return: none
        """
        self.brightness = max(0.0, min(1.0, factor))
        logger.info('Set brightness to: {}%'.format(int(self.brightness * 100)))

    def handle_input_event(self, event_name, num, value):
        logger.debug('input event: {}: {} -> {}'.format(event_name, num, value))
        if event_name == 'playlist_ranged_value':
            self.layers['playlist'].on_ranged_value_change(num, value)
        elif event_name == 'overlay1_ranged_value':
            self.layers['overlay1'].on_ranged_value_change(num, value)
        elif event_name == 'overlay2_ranged_value':
            self.layers['overlay2'].on_ranged_value_change(num, value)
        elif event_name == 'playlist_switch':
            self.layers['playlist'].on_switch_change(num, value)
        elif event_name == 'overlay1_switch':
            self.layers['overlay1'].on_switch_change(num, value)
        elif event_name == 'overlay2_switch':
            self.layers['overlay2'].on_switch_change(num, value)
        else:
            logger.warning('Ignoring unknown event {}'.format(event_name))

    def square_weight_on(self, index):
        if index > 63 or index < 0:
            logger.error("Ignoring square_weight_on() value beyond bounds")
            return
        self.SYNTHETIC_WEIGHTS[index] = 1
        self.SYNTHETIC_WEIGHT_ACTIVE = True

    def square_weight_off(self, index):
        if index > 63 or index < 0:
            logger.error("Ignoring square_weight_on() value beyond bounds")
            return
        self.SYNTHETIC_WEIGHTS[index] = 0

        # Scan the weighs and see if anything is still set
        for value in self.SYNTHETIC_WEIGHTS:
            if value:
                return

        # If nothing is set, there are no longer any synthetic weights active
        self.SYNTHETIC_WEIGHT_ACTIVE = False

    def run_forever(self):
        while True:
            self.run_one_frame()

    @profile(print_seconds=2)
    def run_one_frame(self):
        if not self.playlist.is_running():
            # If the playlist is stopped/paused, sleep a bit then restart the loop
            self.clocksource.sleep(0.5)
            return

        self.init_loop()
        self.prepare()
        self.generate_frame()
        self.transfer_data()
        self.delay()

    @profile()
    def init_loop(self):
        self.frame_start = self.clocksource.time()

    @profile()
    def prepare(self):
        for layer in self._iter_enabled_layers():
            layer.prepare()

    @profile()
    def generate_frame(self):
        context = RenderContext(
            clock=self.frame_start,
            downbeat=self.downbeat,
            weights=self.get_weights(),
            bpm=self.bpm,
        )

        composited_leds = [(0, 0, 0)] * 64
        for layer in self._iter_enabled_layers():
            current_leds = layer.render(context)
            if not current_leds:
                continue
            for idx, current_pixel in enumerate(current_leds):
                current_pixel = normalize_pixel(current_pixel)
                last_pixel = composited_leds[idx]
                composited_leds[idx] = alpha_blend(current_pixel, last_pixel, layer.get_alpha())

        leds = [set_brightness(pixel, self.brightness) for pixel in composited_leds]
        self.driver.set_leds(leds)

    @profile()
    def get_weights(self):
        weights = self.driver.get_weights()
        if self.SYNTHETIC_WEIGHT_ACTIVE:
            for idx in range(64):
                val = self.SYNTHETIC_WEIGHTS[idx]
                if val:
                    weights[idx] = val

        return weights

    @profile()
    def transfer_data(self):
        self.driver.send_data()
        self.driver.read_data()

    @profile()
    def delay(self):
        elapsed = self.clocksource.time() - self.frame_start

        if elapsed < self.frame_seconds:
            self.clocksource.sleep(self.frame_seconds - elapsed)
        else:
            logger.debug("Over by {}".format(elapsed - self.frame_seconds))
