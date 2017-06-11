from base import Base
from util import opc
from util import getch
import threading

CHARS = []
CHAR_MAP = {
    '1': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    'q': 8,
    'w': 9,
    'e': 10,
    'r': 11,
    't': 12,
    'y': 13,
    'u': 14,
    'i': 15,
    'a': 16,
    's': 17,
    'd': 18,
    'f': 19,
    'g': 20,
    'h': 21,
    'j': 22,
    'k': 23,
    'z': 24,
    'x': 25,
    'c': 26,
    'v': 27,
    'b': 28,
    'n': 29,
    'm': 30,
    ',': 31,
    '!': 32,
    '@': 33,
    '#': 34,
    '$': 35,
    '%': 36,
    '^': 37,
    '&': 38,
    '*': 39,
    '<': 63,
}


class Opc(Base):

    MAX_LED_VALUE = 256

    def __init__(self, args):
        super(Opc, self).__init__(args)
        self.frame = 0
        self.ip_port = '127.0.0.1:7890'
        self.client = opc.Client(self.ip_port)

        if self.client.can_connect():
            print('    connected to %s' % self.ip_port)
        else:
            # can't connect, but keep running in case the server appears later
            print('    WARNING: could not connect to {}'.format(self.ip_port))
        print('')

        if self.args['opc_input']:
            self.read_thread = threading.Thread(target=self.read_chars_from_stdin)
            self.read_thread.start()

    @staticmethod
    def read_chars_from_stdin():
        global CHARS

        while True:
            char = getch.getch()
            CHARS.append(char)

            if ord(char) == 3:
                exit(0)

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

    def get_weights(self):
        """
        :return:
        """
        weights = []
        for i in range(0, 64):
            weights.append(0)

        if len(CHARS) > 0:
            for char in CHARS.pop():
                if char in CHAR_MAP:
                    weights[CHAR_MAP[char]] = 1
                elif char.lower() in CHAR_MAP:
                    weights[CHAR_MAP[char.lower()]+32] = 1

                if ord(char) == 3:
                    print "Exiting ...\n"
                    self.read_thread.join()
                    exit(0)

        return weights
