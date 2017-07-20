from base import Base
import importlib
from util import SerialRead

from threading import Thread

import sys


class Raspberry(Base):

    # Define the order in which we output the LEDs.  This could be calculated
    # but spelling it out here to reduce the time to display a frame
    led_order = [
        00,  1,  2,  3,  4,  5,  6,  7,
        15, 14, 13, 12, 11, 10,  9,  8,
        16, 17, 18, 19, 20, 21, 22, 23,
        31, 30, 29, 28, 27, 26, 25, 24,
        32, 33, 34, 35, 36, 37, 38, 39,
        47, 46, 45, 44, 43, 42, 41, 40,
        48, 49, 50, 51, 52, 53, 54, 55,
        63, 62, 61, 60, 59, 58, 57, 56,
    ]

    def __init__(self, args):
        super(Raspberry, self).__init__(args)

        module = importlib.import_module("spidev")

        self.spi = module.SpiDev()
        self.spi.open(0, 0)

        self.worker = Thread(target=self.read_serial_data)
        self.worker.start()

    def send_data(self):
        """
        :return:
        """
        data = list()
        for led in self.led_order:
            rgb = self.leds[led]

            # Repack 3 10-bit values into 4 8-bit values
            data.append(int(rgb[0]) >> 4)
            data.append(((int(rgb[0]) & 0x00F) << 4) | (int(rgb[1]) >> 6))
            data.append(((int(rgb[1]) & 0x3F) << 2) | ((int(rgb[2]) & 0x300) >> 8))
            data.append(int(rgb[2]) & 0x0FF)

        """ DEBUGGING
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
        """

        self.spi.xfer(data)

    def read_data(self):
        """
        The thread running in read_serial_data should be updating the weight values
        :return:
        """
        pass

    def read_serial_data(self):
        reader = SerialRead()
        while True:
            data_bytes = reader.read()
            values = self.process_bytes(data_bytes)

            # Setting a member variable should be atomic
            self.weights = values

    def process_bytes(self, data_bytes):
        new_buf = []
        for packet in range(0, 64):
            hi = ord(data_bytes[packet * 4])
            lo = ord(data_bytes[packet * 4 + 1])
            unsigned_val = (hi << 8) + lo
            signed_val = self.twos_comp(unsigned_val)
            new_buf.append(signed_val)

        return new_buf

    @staticmethod
    def twos_comp(val, bits=10):
        """compute the 2's complement of int value val"""
        if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
            val -= 1 << bits  # compute negative value
        return val
