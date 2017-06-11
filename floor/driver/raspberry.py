from base import Base
import importlib


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
            data.append(rgb[0] >> 4)
            data.append(((rgb[0] & 0x00F) << 4) | (rgb[1] >> 6))
            data.append(((rgb[1] & 0x3F) << 2) | ((rgb[2] & 0x300) >> 8))
            data.append(rgb[2] & 0x0FF)

        self.spi.xfer(data)

    def read_data(self):
        """
        :return:
        """
        pass
