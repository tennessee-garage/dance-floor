import time
import sys
import importlib
import logging
import driver
import pkgutil
import processor

logger = logging.getLogger('controller')


class Controller(object):

    DEFAULT_FPS = 24

    def __init__(self, playlist):
        self.playlist = playlist
        self.driver = None  # type: driver.Base
        self.processor = None  # type: processor.Base
        self.frame_start = 0
        self.fps = None
        self.frame_seconds = None

        self.processors = {}
        self.load_processors()

        self.set_fps(self.DEFAULT_FPS)

    def load_processors(self):
        """Loads (or reloads) all processors."""
        processors = {}
        package = processor
        prefix = package.__name__ + "."
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            if ispkg:
                continue
            basename = modname[len(prefix):]
            try:
                module = self._load_processor(basename, modname)
                processors[basename] = module
            except Exception as e:
                logger.exception('Could not load processor "{}"'.format(basename))

        self.processors = processors

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

    def set_processor(self, processor_name, processor_args=None):
        """Sets the active processor, which must already be loaded into
        `self.processors`.

        Raises `ValueError` if processor is unknown.
        """
        self.processor = self.build_processor(processor_name, processor_args)

    def build_processor(self, name, args=None):
        """Builds a processor instance."""
        processor = self.processors.get(name)
        if not processor:
            raise ValueError('Processor "{}" does not exist'.format(name))
        try:
            return processor.create(args)
        except Exception as e:
            raise ValueError('Processor "{}" could not be created: {}'.format(name, str(e)))

    def set_driver(self, driver_name, driver_args):
        try:
            module = importlib.import_module("driver.{}".format(driver_name))
        except ImportError:
            print "Error: Driver '{}' does not exist or could not be loaded".format(driver_name)
            sys.exit(0)

        self.driver = getattr(module, driver_name.title())(driver_args)

    def run(self):
        while True:
            self.init_loop()
            self.check_playlist()
            self.generate_frame()
            self.transfer_data()
            self.delay()

    def init_loop(self):
        self.frame_start = time.time()

    def check_playlist(self):
        if self.playlist.next_ready():
            self.playlist.advance()
            logger.info('Loading processor {}'.format(self.playlist.get_processor_name()))
            self.set_processor(
                self.playlist.get_processor_name(),
                self.playlist.get_processor_args()
            )
            # Make sure the processor is limited to the bit depth of the driver
            self.processor.set_max_value(self.driver.MAX_LED_VALUE)

    def generate_frame(self):
        leds = self.processor.get_next_frame(self.driver.get_weights())
        self.driver.set_leds(leds)

    def transfer_data(self):
        self.driver.send_data()
        self.driver.read_data()

    def delay(self):
        elapsed = time.time() - self.frame_start
        if elapsed < self.frame_seconds:
            # print "Remain: {}".format(self.frame_seconds - elapsed)
            time.sleep(self.frame_seconds - elapsed)
