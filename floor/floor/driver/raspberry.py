from __future__ import absolute_import
import importlib
import logging

from .base import Base
from floor.util.serial_read import SerialRead

logger = logging.getLogger('raspberry')


class Raspberry(Base):

    # For debugging high frequency loops, only output 1 out of this many times.
    DEBUG_SKIP_RESET = 10

    # The number of bytes in a packet of data for weight values
    WEIGHT_PACKET_SIZE = 2

    # The number of packets in a message from the floor
    WEIGHT_PACKETS = 64

    # Weight sensors are measured using 10-bit ADC.  2^10 - 1 == 1023
    MAX_FLOOR_VALUE = 1023

    # Default minimum value for a floor tile to register as a step.  The weight sensors have a 10-bit
    # range, so this number could be anything from 0 - 1023 with 0 being lowest pressure (nobody stepping)
    # to 1023 (heaviest step).  However note that physical limits and sensor construction limit this
    # to about 700-800 max.
    DEFAULT_FLOOR_THRESHOLD = 200

    # Define the order in which we output the LEDs.  This could be calculated
    # but spelling it out here to reduce the time to display a frame
    TILE_ORDER = [
        00,  1,  2,  3,  4,  5,  6,  7,
        15, 14, 13, 12, 11, 10,  9,  8,
        16, 17, 18, 19, 20, 21, 22, 23,
        31, 30, 29, 28, 27, 26, 25, 24,
        32, 33, 34, 35, 36, 37, 38, 39,
        47, 46, 45, 44, 43, 42, 41, 40,
        48, 49, 50, 51, 52, 53, 54, 55,
        63, 62, 61, 60, 59, 58, 57, 56,
    ]

    NUM_TILES = len(TILE_ORDER)

    def __init__(self, args):
        super(Raspberry, self).__init__(args)

        self.floor_threshold = args.get('floor_threshold', self.DEFAULT_FLOOR_THRESHOLD)

        module = importlib.import_module("spidev")

        # For debugging high frequency loops, only print when this reaches zero (and then reset to DEBUG_SKIP_RESET)
        self.debug_skip_read = 0

        self.spi = module.SpiDev()
        self.spi.open(0, 0)

        self.weights = [0] * self.NUM_TILES

        # The maximum value seen after filtering.
        self.value_ceiling = [0] * self.NUM_TILES
        self.value_floor = [0] * self.NUM_TILES

        self.reader = SerialRead()

    def send_data(self):
        """
        :return:
        """
        data = list()
        for led in self.TILE_ORDER:
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
            position = self.TILE_ORDER[packet]

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
        new_buf = [0] * self.NUM_TILES

        for packet in range(self.WEIGHT_PACKETS):
            value = self.value_from_packet(data_bytes, packet)

            # Use TILE_ORDER to map the single stream back to a left to right, left to right orders
            position = self.TILE_ORDER[packet]

            self.value_ceiling[position] = max(self.value_ceiling[position], value)
            self.value_floor[position] = min(self.value_floor[position], value)

            new_buf[position] = 1 if value else 0

        return new_buf

    def value_from_packet(self, data_bytes, packet):
        idx = packet * self.WEIGHT_PACKET_SIZE
        if idx + 1 >= len(data_bytes):
            return 0

        hi = ord(data_bytes[idx])
        lo = ord(data_bytes[idx + 1])
        value = (hi << 8) + lo

        if value < self.floor_threshold or value > self.MAX_FLOOR_VALUE:
            return 0

        scaled_value = float(value) / self.MAX_FLOOR_VALUE
        return scaled_value
