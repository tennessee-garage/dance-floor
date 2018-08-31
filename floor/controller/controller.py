import time
import sys
import importlib
import logging
import pkgutil
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

        self.processors = {}
        self.load_processors()

        self.current_processor = None
        self.current_args = None

        self.set_fps(self.DEFAULT_FPS)

        self.bpm = None
        self.downbeat = None
        self.set_bpm(self.DEFAULT_BPM)

    def load_processors(self):
        """Loads (or reloads) all processors."""
        package = processor
        prefix = package.__name__ + "."

        # Load or reload all processor modules.
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            if ispkg:
                continue
            basename = modname[len(prefix):]
            try:
                module = self._load_processor(basename, modname)
            except Exception as e:
                logger.exception('Could not load processor "{}"'.format(basename))

        # Regenerate processor map
        new_processors = {}
        for p in processor.Base.__subclasses__():
            new_processors[p.__name__.lower()] = p
        self.processors = new_processors

    def _load_processor(self, base_name, module_name):
        module = None
        if base_name in self.processors:
            module = reload(module_name)
            logger.info('Reloaded processor "{}"'.format(base_name))
        else:
            module = importlib.import_module(module_name)
            logger.info('Loaded processor "{}"'.format(base_name))
        return module

    def set_fps(self, fps):
        self.fps = fps
        self.frame_seconds = 1.0/fps

    def set_bpm(self, bpm, downbeat=None):
        logger.info('Setting bpm to: {}'.format(bpm))
        self.bpm = float(bpm)
        self.downbeat = downbeat or time.time()
        if self.processor:
            self.processor.set_bpm(bpm, self.downbeat)

    def set_processor(self, processor_name, processor_args=None):
        """Sets the active processor, which must already be loaded into
        `self.processors`.

        Raises `ValueError` if processor is unknown.
        """
        self.processor = self.build_processor(processor_name, processor_args)
        self.processor.set_bpm(self.bpm, self.downbeat)
        self.current_processor = processor_name
        self.current_args = processor_args

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
            module = importlib.import_module("driver.{}".format(driver_name))
        except ImportError as e:
            print "Error: Driver '{}' does not exist or could not be loaded: {}".format(driver_name, e)
            sys.exit(0)

        self.driver = getattr(module, driver_name.title())(driver_args)
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
            self.processor.set_max_value(self.driver.MAX_LED_VALUE)

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
            # print "Remain: {}".format(self.frame_seconds - elapsed)
            time.sleep(self.frame_seconds - elapsed)
