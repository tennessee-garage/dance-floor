

class Base(object):

    def __init__(self, driver_args):
        self.weights = []
        self.leds = [[0, 0, 0, 0] for _ in range(64)]
        self.args = driver_args

        if "layout" in driver_args:
            self.layout = driver_args["layout"]
        else:
            self.layout = None

    def get_weights(self):
        """
        Returns the last retrieved list of weight values.

        Weights are a value between 0.0 and 1.0.
        """
        return self.weights

    def set_leds(self, values):
        """
        Set a list of LED objects representing the next set of color values
        :param values:
        :return:
        """
        self.leds = values

    def test_support(self):
        """
        Overridden by driver; tests to make sure current platform supports driver
        :return:
        """
        pass

    def send_data(self):
        """
        Overridden by driver; sends data to hardware
        :return:
        """
        pass

    def read_data(self):
        """
        Overridden by driver; reads and sets self.weights with result
        :return:
        """
        pass
