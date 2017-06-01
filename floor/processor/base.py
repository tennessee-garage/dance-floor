

class Base(object):

    DEFAULT_MAX_VALUE = 1024

    def __init__(self):
        self.weights = []
        self.max_value = self.DEFAULT_MAX_VALUE

    def set_max_value(self, max_value):
        self.max_value = max_value

    def get_next_frame(self, weights):
        """
        Generate the LED values needed for the next frame
        :return:
        """
        pass
