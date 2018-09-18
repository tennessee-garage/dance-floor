from base import Base
import importlib
from util.serial_read import SerialRead

import logging

logger = logging.getLogger('raspberry')


class Raspberry(Base):

    # For debugging high frequency loops, only output 1 out of this many times.
    DEBUG_SKIP_RESET = 10

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

    # Minimum value for a floor tile to register.  Anything under this will be treated as zero
    floor_minimum = 10

    def __init__(self, args):
        super(Raspberry, self).__init__(args)

        module = importlib.import_module("spidev")

        # For debugging high frequency loops, only print when this reaches zero (and then reset to DEBUG_SKIP_RESET)
        self.debug_skip_read = 0

        self.spi = module.SpiDev()
        self.spi.open(0, 0)

        self.weights = [0 for _ in range(64)]

        # The maximum value seen after filtering.
        self.value_ceiling = [0 for _ in range(64)]
        self.value_floor = [0 for _ in range(64)]

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

        self.print_weights(values)

        # Setting a member variable should be atomic
        self.weights = values

        self.debug_skip_read -= 1
        if self.debug_skip_read < 0:
            self.debug_skip_read = self.DEBUG_SKIP_RESET

    def get_weights(self):
        return self.weights

    def print_weights(self, values):
        # Only output 1 out of DEBUG_SKIP_RESET times
        if self.debug_skip_read != 0:
            return

        # Skip all this processing if we aren't going to output anything in the end
        if logger.getEffectiveLevel() > logging.DEBUG:
            return

        log_line = "\n | "

        for packet in range(self.WEIGHT_PACKETS):
            position = self.tile_order[packet]

            log_line += "{}: {:>2} ({:>2}/{:>2}) | ".format(
                    position,
                    values[position],
                    self.value_floor[position],
                    self.value_ceiling[position]
                )

            if packet % 8 == 7:
                log_line += " | \n"

        log_line += "-----------------------------------------\n"
        logger.debug(log_line)

    def process_bytes(self, data_bytes):
        # Pre-fill a 64 byte list
        new_buf = [0 for _ in range(self.WEIGHT_PACKETS)]

        for packet in range(self.WEIGHT_PACKETS):
            value = self.value_from_packet(data_bytes, packet)

            # Use tile_order to map the single stream back to a left to right, left to right orders
            position = self.tile_order[packet]
            adjusted_val = self.adjust_value(value)

            self.value_ceiling[position] = max(self.value_ceiling[position], adjusted_val)
            self.value_floor[position] = min(self.value_floor[position], adjusted_val)

            new_buf[position] = adjusted_val

        return new_buf

    def value_from_packet(self, data_bytes, packet):
        idx = packet * self.WEIGHT_PACKET_SIZE
        if idx + 1 >= len(data_bytes):
            return 0

        hi = ord(data_bytes[idx])
        lo = ord(data_bytes[idx + 1])
        unsigned_val = (hi << 8) + lo
        return self.twos_comp(unsigned_val)

    @staticmethod
    def twos_comp(val, bits=10):
        """compute the 2's complement of int value val"""
        if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
            val -= 1 << bits  # compute negative value
        return val

    def adjust_value(self, value):
        if value <= self.floor_minimum:
            return 0
        else:
            return value
