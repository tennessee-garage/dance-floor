import driver


class Test(object):

    def __init__(self):
        self.driver = driver.Raspberry([])

    def run(self, leds):
        self.driver.set_leds(leds)
        self.driver.send_data()
        self.driver.read_data()
