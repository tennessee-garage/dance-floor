import serial
import sys


class SerialRead:

    packets = 64
    packet_bytes = 2
    data_bytes = packet_bytes * packets

    # Don't start reading until there are a number of bytes ready
    buffer_bytes = 1024

    port = "/dev/ttyS0"
    baud = 57600
    bits = serial.EIGHTBITS
    stop_bits = serial.STOPBITS_ONE

    def __init__(self):
        self.ser = serial.Serial(
            self.port,
            baudrate=self.baud,
            bytesize=self.bits,
            timeout=None,
            stopbits=self.stop_bits
        )

        # Read data up to the next stop marker
        self.synchronize()

    @staticmethod
    def is_stop_marker(val):
        # The first 6 bits of the first byte should always be zero for normal data so this condition is unique
        return val[0] == chr(0xFF) and val[1] == chr(0xFF)

    def generate_null_packet(self):
        return [chr(0) for _ in range(self.packet_bytes)]

    def synchronize(self):
        """
        Read data until we find a stop packet to sync ourselves up to the data being sent
        :return:
        """

        if not self.data_ready():
            return

        packet = self.generate_null_packet()
        while True:
            val = self.ser.read(1)
            # Treat packet as a FIFO until we match a stop marker
            packet = packet[1:] + [val]

            if self.is_stop_marker(packet):
                return

    def data_ready(self):
        return self.ser.inWaiting() > self.buffer_bytes

    def read(self):
        buf = []
        val = self.generate_null_packet()

        while not self.is_stop_marker(val):
            val = self.ser.read(self.packet_bytes)
            buf.extend(val)
            # for c in val:
            #     sys.stdout.write("{} ".format(ord(c)))
            #     sys.stdout.flush()

        # Clip out and return only the last self.data_bytes before the stop packet
        start_index = len(buf) - (self.data_bytes+self.packet_bytes)
        end_index = len(buf) - self.packet_bytes
        return buf[start_index:end_index]
