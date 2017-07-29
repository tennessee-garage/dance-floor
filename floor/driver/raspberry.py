from base import Base
import importlib
from util.serial_read import SerialRead
import time
from threading import Thread

import logging

logger = logging.getLogger('raspberry')


class Raspberry(Base):

    # The number of bytes in a packet of data for weight values
    WEIGHT_PACKET_SIZE = 2

    # The number of packets in a message from the floor
    WEIGHT_PACKETS = 64

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
    floor_minimum = 10

    def __init__(self, args):
        super(Raspberry, self).__init__(args)

        module = importlib.import_module("spidev")

        self.spi = module.SpiDev()
        self.spi.open(0, 0)

        self.weights = [0 for _ in range(64)]

        # How often to take a sample of the current minimum floor value to (auto-tare)
        self.next_sample = time.time() + self.floor_period

        # Keep track of the last self.floor_sample raw values seen over the past self.floor_period seconds.  These
        # are the actual values returned from the floor and will vary from slightly negative to slightly positive
        self.value_floor = [[0] for _ in range(64)]

        self.start_time = time.time()
        # The maximum value seen after filtering.
        self.value_ceiling = [0 for _ in range(64)]

        # Keep track of the last self.floor_sample adjusted values.  Only report a step if they are non-zero
        # for the full history
        self.value_history = [[0] for _ in range(64)]

        self.reader = SerialRead()

        # logger.info("Staring serial worker")
        # self.worker = Thread(target=self.read_serial_data)
        # self.worker.daemon = True
        # self.worker.start()

    def send_data(self):
        """
        :return:
        """
        data = list()
        for led in self.tile_order:

            # Don't add this data to the list if this tile has been bypassed
            if self.layout and self.layout.is_bypassed(led):
                continue

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

        # Read whatever we can
        self.reader.read()

        if not self.reader.data_ready:
            return

        data_bytes = self.reader.get_frame()
        values = self.process_bytes(data_bytes)

        #self.print_weights(values)

        # Setting a member variable should be atomic
        self.weights = values

    def get_weights(self):
        return self.weights

    def print_weights(self, values):

        log_line = " | "

        for packet in range(self.WEIGHT_PACKETS):
            position = self.tile_order[packet]

            log_line += "{}: {:>2} ({:>2}/{:>2}) | ".format(
                    position,
                    values[position],
                    min(self.value_floor[position]),
                    self.value_ceiling[position]
                )

            if packet % 8 == 7:
                logger.info(log_line)
                log_line = " | "

        logger.info("(1, 8): {} ({})".format(
            self.value_floor[56],
            1.0*sum(self.value_floor[56])/len(self.value_floor[56])
        ))
        logger.info("-----------------------------------------\n")

    def process_bytes(self, data_bytes):
        # Pre-fill a 64 byte list
        new_buf = [0 for _ in range(self.WEIGHT_PACKETS)]

        sample = False
        if time.time() >= self.next_sample:
            sample = True
            self.next_sample = time.time() + self.floor_period

        for packet in range(self.WEIGHT_PACKETS):
            hi = ord(data_bytes[packet * self.WEIGHT_PACKET_SIZE])
            lo = ord(data_bytes[packet * self.WEIGHT_PACKET_SIZE + 1])
            unsigned_val = (hi << 8) + lo
            signed_val = self.twos_comp(unsigned_val)

            # Use tile_order to map the single stream back to a left to right, left to right orders
            position = self.tile_order[packet]
            adjusted_val = self.adjust_value(signed_val, position, sample)

            if (time.time() - self.start_time > 5) and (self.value_ceiling[position] < adjusted_val):
                self.value_ceiling[position] = adjusted_val

            new_buf[position] = self.filter_value(adjusted_val, position)

        return new_buf

    def adjust_value(self, value, position, sample):

        # See if self.floor_period seconds have elapsed
        if sample:

            # See if we have a full set of samples yet
            if len(self.value_floor[position]) < self.floor_samples:
                self.value_floor[position].append(value)
            else:
                # Shift in the new value and re-sort low to high
                self.value_floor[position] = self.value_floor[position][1:] + [value]

        # Subtract the lowest value we've seen for this position over the
        # last self.floor_period * self.floor_samples seconds
        value -= min(self.value_floor[position])
        if value <= self.floor_minimum:
            return 0
        else:
            return value

    def filter_value(self, value, position):
        if len(self.value_history[position]) < self.floor_samples:
            self.value_history[position].append(value)
        else:
            self.value_history[position] = self.value_history[position][1:] + [value]

        for v in self.value_history[position]:
            # If there are ANY zero values, ignore this for now
            if v == 0:
                return 0

        # If all values in recent history are greater than zero, then return this value
        return value

    @staticmethod
    def twos_comp(val, bits=10):
        """compute the 2's complement of int value val"""
        if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
            val -= 1 << bits  # compute negative value
        return val
