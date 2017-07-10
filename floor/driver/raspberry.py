from base import Base
import importlib
import sys


class Raspberry(Base):

    def __init__(self, args):
        super(Raspberry, self).__init__(args)

        module = importlib.import_module("spidev")

        self.spi = module.SpiDev()
        self.spi.open(0, 0)

    def send_data(self):
        """
        :return:
        """
        data = list()
        for rgb in self.leds:
            # Repack 3 10-bit values into 4 8-bit values
            data.append(int(rgb[0]) >> 4)
            data.append(((int(rgb[0]) & 0x00F) << 4) | (int(rgb[1]) >> 6))
            data.append(((int(rgb[1]) & 0x3F) << 2) | ((int(rgb[2]) & 0x300) >> 8))
            data.append(int(rgb[2]) & 0x0FF)

        byte = 0
        square = 0
        for v in data:
            if byte == 0:
                sys.stdout.write("{:02d})".format(square))
                square += 1

            sys.stdout.write(" / {:02x}".format(v))

            byte = (byte + 1) % 4
            if byte == 0:
                print("")

        self.spi.xfer(data)

    def read_data(self):
        """
        :return:
        """
        pass
