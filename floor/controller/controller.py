import time
import sys
import importlib
import driver
import processor


class Controller(object):

    DEFAULT_FPS = 24

    def __init__(self):
        self.driver = None  # type: driver.Base
        self.processor = None  # type: processor.Base
        self.frame_start = 0
        self.fps = None
        self.frame_seconds = None

        self.set_fps(self.DEFAULT_FPS)

    def set_fps(self, fps):
        self.fps = fps
        self.frame_seconds = 1.0/fps

    def set_processor(self, processor_name):

        try:
            module = importlib.import_module("processor.{}".format(processor_name))
        except ImportError:
            print "Error: Processor '{}' does not exist or could not be loaded".format(processor_name)
            sys.exit(0)

        self.processor = module.create()

    def set_driver(self, driver_name, driver_args):

        try:
            module = importlib.import_module("driver.{}".format(driver_name))
        except ImportError:
            print "Error: Driver '{}' does not exist or could not be loaded".format(driver_name)
            sys.exit(0)

        self.driver = getattr(module, driver_name.title())(driver_args)

    def run(self):
        # Make sure the processor is limited to the bit depth of the driver
        self.processor.set_max_value(self.driver.MAX_LED_VALUE)

        while True:
            self.init_loop()
            self.generate_frame()
            self.transfer_data()
            self.delay()

    def init_loop(self):
        self.frame_start = time.time()

    def generate_frame(self):
        leds = self.processor.get_next_frame(self.driver.get_weights())
        self.driver.set_leds(leds)

    def transfer_data(self):
        self.driver.send_data()
        self.driver.read_data()

    def delay(self):
        elapsed = time.time() - self.frame_start
        if elapsed < self.frame_seconds:
            time.sleep(self.frame_seconds - elapsed)
