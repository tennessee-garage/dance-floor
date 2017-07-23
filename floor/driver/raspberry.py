from base import Base
import importlib
from util.serial_read import SerialRead
import time

from threading import Thread

import sys


class Raspberry(Base):

    # Define the order in which we output the LEDs.  This could be calculated
    # but spelling it out here to reduce the time to display a frame
    tile_order = [
        00,  1,  2,  3,  4,  5,  6,  7,
        15, 14, 13, 12, 11, 10,  9,  8,
        16, 17, 18, 19, 20, 21, 22, 23,
        31, 30, 29, 28, 27, 26, 25, 24,
        32, 33, 34, 35, 36, 37, 38, 39,
        47, 46, 45, 44, 43, 42, 41, 40,
        48, 49, 50, 51, 52, 53, 54, 55,
        63, 62, 61, 60, 59, 58, 57, 56,
    ]

    # Take a floor sample every floor_period seconds
    floor_period = 5

    # Keep a maximum of floor_sample samples
    floor_samples = 5

    # Minimum value for a floor tile to register.  Anything under this will be treated as zero
    floor_minimum = 5

    def __init__(self, args):
        super(Raspberry, self).__init__(args)

        module = importlib.import_module("spidev")

        self.spi = module.SpiDev()
        self.spi.open(0, 0)

        self.weights = [0 for _ in range(64)]

        # Keep track of the last self.floor_sample values seen over the past self.floor_period seconds
        self.value_floor = [[0] for _ in range(64)]

        self.worker = Thread(target=self.read_serial_data)
        self.worker.daemon = True
        self.worker.start()

    def send_data(self):
        """
        :return:
        """
        data = list()
        for led in self.tile_order:
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

    def get_weights(self):
        return self.weights

    def read_serial_data(self):
        reader = SerialRead()
        while True:
            data_bytes = reader.read()
            values = self.process_bytes(data_bytes)
            values = self.pad_values(values)

            # self.print_weights(values)

            # Setting a member variable should be atomic
            self.weights = values

    @staticmethod
    def print_weights(values):
        for x in range(8):
            sys.stdout.write(" | ")
            for y in range(8):
                sys.stdout.write("{:>3} | ".format(values[x*8 + y]))
            sys.stdout.write("\n")

        sys.stdout.write("-----------------------------------------\n")
        sys.stdout.flush()

    def process_bytes(self, data_bytes):
        # Pre-fill a 64 byte list
        new_buf = [0 for _ in range(64)]

        for packet in range(64):
            if len(data_bytes) <= packet * 4:
                print "LENGTH: {}".format(len(data_bytes))

            hi = ord(data_bytes[packet * 4])
            lo = ord(data_bytes[packet * 4 + 1])
            unsigned_val = (hi << 8) + lo
            signed_val = self.twos_comp(unsigned_val)

            # Use tile_order to map the single stream back to a left to right, left to right orders
            position = self.tile_order[packet]
            new_buf[position] = self.adjust_value(signed_val, position)

        return new_buf

    def adjust_value(self, value, position):
        # See if self.floor_period seconds have elapsed
        if int(time.time()) % self.floor_period == 0:

            # See if we have a full set of samples yet
            if len(self.value_floor[position]) < self.floor_samples:
                self.value_floor[position].append(value)
            else:
                # Shift in the new value and re-sort low to high
                self.value_floor[position] = self.value_floor[position][1:] + [value]

            self.value_floor[position].sort()
            # sys.stdout.write("{}) ".format(position))
            # print self.value_floor[position]

        # Subtract the lowest value we've seen for this position over the
        # last self.floor_period * self.floor_samples seconds
        value -= self.value_floor[position][0]
        if value <= self.floor_minimum:
            return 0
        else:
            return value

    @staticmethod
    def twos_comp(val, bits=10):
        """compute the 2's complement of int value val"""
        if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
            val -= 1 << bits  # compute negative value
        return val

    @staticmethod
    def pad_values(values):
        """
        Temporary padding to toss out bogus weight values when there aren't a full set of 64 squares
        :param values:
        :return:
        """
        padded = [0 for _ in range(48)]
        padded.extend(values[0:16])
        return padded
