import importlib
import logging
import time

logger = logging.getLogger("test")


class Test:
    def __init__(self):
        driver_name = "raspberry"

        try:
            module = importlib.import_module(f"floor.driver.{driver_name}")
        except ImportError as e:
            print(f"Error: Driver '{driver_name}' does not exist or could not be loaded: {e}")
            raise

        self.driver = getattr(module, driver_name.title())({})

    def run(self, leds):
        self.driver.set_leds(leds)
        self.driver.send_data()

        timeout = 1
        start_time = time.time()
        while not self.driver.read_data():
            if time.time() > start_time + timeout:
                logger.info("Timed out waiting for data from the floor")
                return
