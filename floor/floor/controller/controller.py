from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time
import logging
from collections import OrderedDict

from floor import processor
from floor.processor.base import RenderContext
from floor.controller.rendering import PlaylistRenderLayer
from floor.controller.rendering import ProcessorRenderLayer
from floor.util.color_utils import blend_pixel_nonalpha

logger = logging.getLogger('controller')


class Controller(object):
    DEFAULT_FPS = 120
    DEFAULT_BPM = 120.0
    MAX_RANGED_VALUES = 4

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

        self.ranged_values = [0] * self.MAX_RANGED_VALUES

    def _iter_enabled_layers(self):
        """Returns an iterable of all enabled layers."""
        return filter(lambda layer: layer.is_enabled(), self.layers.values())

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

    def square_weight_on(self, index):
        if index > 63 or index < 0:
            logger.error("Ignoring square_weight_on() value beyond bounds")
            return
        self.SYNTHETIC_WEIGHTS[index] = 1.0
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

    def handle_ranged_value(self, control_number, control_value):
        if control_number > self.MAX_RANGED_VALUES:
            logger.warning('Ignoring MIDI control {}, greater than {}'.format(control_number, self.MAX_RANGED_VALUES))

        # Capture state.
        self.ranged_values[control_number] = control_value
        # Update current processor.
        for layer in self._iter_enabled_layers():
            layer.on_ranged_value_change(control_number, control_value)

    def run_forever(self):
        while True:
            self.run_one_frame()

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

    def init_loop(self):
        self.frame_start = self.clocksource.time()

    def prepare(self):
        for layer in self._iter_enabled_layers():
            layer.prepare()

    def generate_frame(self):
        context = RenderContext(
            clock=self.frame_start,
            downbeat=self.downbeat,
            weights=self.get_weights(),
            bpm=self.bpm,
        )

        leds = None
        last_leds = None
        for layer in self._iter_enabled_layers():
            leds = layer.render(context, leds=last_leds)
            if leds and last_leds:
                # Copy the returned buffer, since we'll likely be blending into it
                # and cannot assume ownership.
                leds = leds[:]
                for idx, last_pixel in enumerate(last_leds):
                    leds[idx] = blend_pixel_nonalpha(last_pixel, leds[idx])
            last_leds = leds

        # If no layers are enabled, `leds` will be None and we shouldn't update the driver.
        # TODO(mikey): Should we render a 'default' pattern in this case?
        if leds:
            leds = map(lambda pixel: map(lambda color: color * self.brightness, pixel), leds)
            self.driver.set_leds(leds)

    def get_weights(self):
        weights = self.driver.get_weights()
        if self.SYNTHETIC_WEIGHT_ACTIVE:
            for idx in range(64):
                val = self.SYNTHETIC_WEIGHTS[idx]
                if val:
                    weights[idx] = val

        return weights

    def transfer_data(self):
        self.driver.send_data()
        self.driver.read_data()

    def delay(self):
        elapsed = self.clocksource.time() - self.frame_start

        if elapsed < self.frame_seconds:
            self.clocksource.sleep(self.frame_seconds - elapsed)
        else:
            logger.debug("Over by {}".format(elapsed - self.frame_seconds))
