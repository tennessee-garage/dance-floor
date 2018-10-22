import time
import sys
import importlib
import logging
from floor import driver
from floor import processor

logger = logging.getLogger('controller')


class Controller(object):
    DEFAULT_FPS = 24
    DEFAULT_BPM = 120.0

    def __init__(self, playlist):
        self.playlist = playlist
        self.driver = None  # type: driver.Base
        self.processor = None  # type: processor.Base
        self.frame_start = 0
        self.fps = None
        self.frame_seconds = None

        self.processors = processor.all_processors()

        # The name of the current processor
        self.current_processor = None
        self.current_args = None

        self.set_fps(self.DEFAULT_FPS)

        self.bpm = None
        self.downbeat = None
        self.set_bpm(self.DEFAULT_BPM)

        # Max value is dictated by the driver used
        self.max_led_value = None
        # Effective max value accounts for any scaling factor in effect (e.g. to reduce brightness)
        self.max_effective_led_value = None

    def set_fps(self, fps):
        self.fps = fps
        self.frame_seconds = 1.0/fps

    def set_bpm(self, bpm, downbeat=None):
        logger.info('Setting bpm to: {}'.format(bpm))
        self.bpm = float(bpm)
        self.downbeat = downbeat or time.time()
        if self.processor:
            self.processor.set_bpm(bpm, self.downbeat)

    def scale_brightness(self, factor):
        """Scale the default brightness from 0 to max for driver

        :param factor: a scaling factor from 0.0 to 1.0
        :return: none
        """
        new_max = factor * self.driver.MAX_LED_VALUE
        self.processor.set_max_value(new_max)

    def set_processor(self, processor_name, processor_args=dict):
        """Sets the active processor, which must already be loaded into
        `self.processors`.

        Raises `ValueError` if processor is unknown.
        """
        self.processor = self.build_processor(processor_name, processor_args)
        self.processor.set_bpm(self.bpm, self.downbeat)

        fps = self.processor.requested_fps() or self.DEFAULT_FPS
        self.set_fps(fps)

        self.current_processor = processor_name
        self.current_args = processor_args

        logger.info("Started processor '{}' at {} fps".format(processor_name, fps))

    def build_processor(self, name, args=None):
        """Builds a processor instance."""
        args = args or {}
        processor = self.processors.get(name)
        if not processor:
            raise ValueError('Processor "{}" does not exist'.format(name))
        try:
            return processor(**args)
        except Exception as e:
            raise ValueError('Processor "{}" could not be created: {}'.format(name, str(e)))

    def set_driver(self, driver_name, driver_args):
        try:
            module = importlib.import_module("floor.driver.{}".format(driver_name))
        except ImportError as e:
            print "Error: Driver '{}' does not exist or could not be loaded: {}".format(driver_name, e)
            sys.exit(0)

        self.driver = getattr(module, driver_name.title())(driver_args)
        self.max_led_value = self.driver.MAX_LED_VALUE
        self.max_effective_led_value = self.max_led_value
        logger.info("Loaded driver '{}' with max LED value {}".format(driver_name, self.driver.MAX_LED_VALUE))

    def run(self):
        while True:
            if not self.playlist.is_running():
                # If the playlist is stopped/paused, sleep a bit then restart the loop
                time.sleep(0.5)
                continue

            self.init_loop()
            self.check_playlist()
            self.generate_frame()
            self.transfer_data()
            self.delay()

    def init_loop(self):
        self.frame_start = time.time()

    def check_playlist(self):
        item = self.playlist.get_current()
        if not item:
            return

        processor, args = item['name'], item['args']
        if processor not in self.processors:
            logger.error('Unknown processor "{}"; removing it.'.format(processor))
            self.playlist.remove(self.playlist.position)
            return

        if processor and (processor, args) != (self.current_processor, self.current_args):
            logger.debug('Loading processor {}'.format(processor))
            self.set_processor(processor, args)
            # Make sure the processor is limited to the bit depth of the driver
            self.processor.set_max_value(self.max_effective_led_value)

    def generate_frame(self):
        if not self.processor:
            return
        try:
            leds = self.processor.get_next_frame(self.driver.get_weights())
        except KeyboardInterrupt:
            raise
        except Exception:
            logger.exception('Error generating frame for processor {}'.format(self.processor))
            logger.warning('Removing processor due to error.')
            self.playlist.remove(self.playlist.position)
        else:
            self.driver.set_leds(leds)

    def transfer_data(self):
        self.driver.send_data()
        self.driver.read_data()

    def delay(self):
        elapsed = time.time() - self.frame_start

        if elapsed < self.frame_seconds:
            time.sleep(self.frame_seconds - elapsed)
        else:
            logger.debug("Over by {}".format(elapsed - self.frame_seconds))
