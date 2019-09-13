from builtins import range
from builtins import object

from floor.controller import Layout


class Base(object):

    def __init__(self, driver_args):
        self.weights = []
        self.leds = [[0, 0, 0, 0] for _ in range(64)]
        self.args = driver_args
        self.layout = None

    def init_layout(self, layout_name=None):
        if layout_name:
            self.layout = Layout(config_dir=self.args.config_dir,
                                 config_name=layout_name)
        else:
            num_squares = self.probe_floor()
            self.layout = Layout.from_squares(config_dir=self.args['config_dir'],
                                              num_squares=num_squares)

    def probe_floor(self):
        return 64

    def get_weights(self):
        """
        Returns the last retrieved list of weight values.

        Weights are an integer, either 0 (off) or 1 (on).
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
