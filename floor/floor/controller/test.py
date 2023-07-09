from __future__ import print_function

import importlib
from builtins import object


class Test(object):
    def __init__(self):
        driver_name = "raspberry"

        try:
            module = importlib.import_module("floor.driver.{}".format(driver_name))
        except ImportError as e:
            print(
                "Error: Driver '{}' does not exist or could not be loaded: {}".format(
                    driver_name, e
                )
            )
            raise

        self.driver = getattr(module, driver_name.title())({})

    def run(self, leds):
        self.driver.set_leds(leds)
        self.driver.send_data()
        self.driver.read_data()
