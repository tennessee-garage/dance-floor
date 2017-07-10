

class Base(object):

    DEFAULT_MAX_VALUE = 1024
    FLOOR_WIDTH = 8
    FLOOR_HEIGHT = 8

    def __init__(self, args=dict):
        self.weights = []
        self.max_value = self.DEFAULT_MAX_VALUE
        self.args = args

    # accept (x,y) tuple reflecting a coordinate
    # return the array index suitable for use in weights or pixels arrays
    def idx(self,pixel):
        (x,y) = pixel
        return (x * self.FLOOR_WIDTH) + y

    def set_max_value(self, max_value):
        self.max_value = max_value

    def get_next_frame(self, weights):
        """
        Generate the LED values needed for the next frame
        :return:
        """
        pass
