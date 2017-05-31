

class Base(object):

    def __init__(self):
        self.weights = []
        self.leds = []

    def get_weights(self):
        """
        Returns the last retrieved list of weight values
        :return:
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
