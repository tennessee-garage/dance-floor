import serial


class SerialRead:

    data_bytes = 256
    packet_bytes = 4

    port = "/dev/ttyS0"
    baud = 9600
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
        # The last two bytes should always be zero for normal data so this condition is unique
        return val[0] == 's' and val[1] == 't' and val[2] == 'o' and val[3] == 'p'

    def generate_null_packet(self):
        return [chr(0) for _ in range(self.packet_bytes)]

    def synchronize(self):
        """
        Read data until we find a stop packet to sync ourselves up to the data being sent
        :return:
        """
        packet = self.generate_null_packet()
        while True:
            val = self.ser.read(1)
            # Treat packet as a FIFO until we match a stop marker
            packet = packet[1:] + [val]

            if self.is_stop_marker(packet):
                return

    def read(self):
        buf = []
        val = self.generate_null_packet()

        while not self.is_stop_marker(val):
            val = self.ser.read(4)
            buf.extend(val)

        # Clip out and return only the last self.data_bytes before the stop packet
        start_index = len(buf) - (self.data_bytes+self.packet_bytes)
        end_index = len(buf) - self.packet_bytes
        return buf[start_index:end_index]
