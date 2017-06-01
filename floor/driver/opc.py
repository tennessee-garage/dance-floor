from base import Base
from util import opc


class Opc(Base):

    MAX_LED_VALUE = 256

    def __init__(self):
        super(Opc, self).__init__()
        self.frame = 0
        self.ip_port = '127.0.0.1:7890'
        self.client = opc.Client(self.ip_port)

        if self.client.can_connect():
            print('    connected to %s' % self.ip_port)
        else:
            # can't connect, but keep running in case the server appears later
            print('    WARNING: could not connect to {}'.format(self.ip_port))
        print('')

    def send_data(self):
        """
        :return:
        """
        self.client.put_pixels(self.leds, channel=0)

    def read_data(self):
        """
        :return:
        """
        pass
