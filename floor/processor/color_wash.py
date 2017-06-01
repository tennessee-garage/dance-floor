from base import Base


class Color_Wash(Base):
    def __init__(self):
        super(Color_Wash, self).__init__()
        self.red = 0
        self.green = 0
        self.blue = 0

    def get_next_frame(self, weights):
        # Ignore weights

        pixels = []

        for x in range(0, 8):
            for y in range(0, 8):
                pixels.append((
                    (self.red * x) % self.max_value,
                    (self.green * y) % self.max_value,
                    self.blue % self.max_value
                ))

        self.red += 1
        self.green += 1
        self.blue += 1

        return pixels
