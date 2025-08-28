from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame

class SPI10bitPacketExtractor(HighLevelAnalyzer):
    result_types = {
        'packet': {
            'format': 'R: {a}, G: {b}, B: {c}'
        }
    }

    def __init__(self):
        self.buffer = []
        self.start_time = None

    def decode(self, frame: AnalyzerFrame):
        # Only process SPI data frames
        if frame.type != 'data':
            return None

        # Save the first frame start time to assign to the packet later
        if self.start_time is None:
            self.start_time = frame.start_time

        self.buffer.append(frame.data['data'])

        # Wait until we have 4 bytes
        if len(self.buffer) < 4:
            return None

        # Combine the 4 bytes into a single 32-bit integer
        combined = (
            (self.buffer[0] << 24) |
            (self.buffer[1] << 16) |
            (self.buffer[2] << 8) |
            (self.buffer[3])
        )

        # Extract three 10-bit numbers
        r = combined & 0x3FF  # Bits 0-9
        g = (combined >> 10) & 0x3FF  # Bits 10-19
        b = (combined >> 20) & 0x3FF  # Bits 20-29

        # Prepare output frame
        result = AnalyzerFrame(
            'packet',
            self.start_time,
            frame.end_time,
            {
                'r': r,
                'g': g,
                'b': b
            }
        )

        # Reset for next packet
        self.buffer.clear()
        self.start_time = None

        return result