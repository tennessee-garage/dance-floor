import serial


class SerialRead:

    packets = 64
    packet_bytes = 2
    frame_bytes = packet_bytes * packets

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

        self.read_buffer = []
        self.data_ready = False

    def synchronize(self):
        """
        Read data until we find a stop packet to sync ourselves up to the data being sent
        :return:
        """

        if not self.data_ready:
            return

        packet = self.generate_null_packet()
        while True:
            val = self.ser.read(1)
            # Treat packet as a FIFO until we match a stop marker
            packet = packet[1:] + [val]

            if self.is_stop_marker(packet):
                return

    @staticmethod
    def is_stop_marker(val):
        # The first 6 bits of the first byte should always be zero for normal data so this condition is unique
        return val[0] == chr(0xFF) and val[1] == chr(0xFF)

    def generate_null_packet(self):
        return [chr(0) for _ in range(self.packet_bytes)]

    def read(self):
        # If the data is ready, wait for it to be read before collecting more
        if self.data_ready:
            return

        available = self.ser.inWaiting()

        while available > 0:
            data = self.ser.read(self.packet_bytes)
            available -= 2

            if self.is_stop_marker(data):
                self.data_ready = True
                return

            self.read_buffer.extend(data)

    def get_frame(self):
        # Reset this ready state for the next round
        self.data_ready = False

        # Return only the last self.frame_bytes (in case we got extra)
        start_index = len(self.read_buffer) - self.frame_bytes
        return self.read_buffer[start_index:]
