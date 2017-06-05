from base import Base
from fonts import synchronizer


def create():
    return Message()


class Message(Base):

    # How far apart should the letters be
    KERNING = 1
    # Essentially the width of the dance floor
    WINDOW_WIDTH = 8

    def __init__(self):
        super(Message, self).__init__()
        self.font = synchronizer.alpha()
        # The text of the message to scroll
        self.mesg = "The quick brown fox jumps over the lazy dog"
        # The message converted to the font in an array
        self.wall = []
        # The current window position on the wall
        self.window = 0.0
        # How fast to scroll in pixels per frame
        self.speed = 0.5

        self.init_wall(self.mesg)

    def init_wall(self, mesg):
        for row in range(0, 8):
            self.wall.append([])

            # Add blank space at the beginning so the text can scroll in from the side
            self.wall[row].extend([0] * self.WINDOW_WIDTH)

            # Add the characters for this row
            for char in list(mesg):
                width = self.font[char][0]
                row_data = self.font[char][row+1]

                # Add this strip of the character to the wall
                self.wall[row].extend(row_data)
                # Add kerning
                self.wall[row].extend([0] * self.KERNING)

            # Add blank space at the end so the text can scroll off the side, minus the
            # kerning from the final letter
            self.wall[row].extend([0] * (self.WINDOW_WIDTH - self.KERNING))

    def get_next_frame(self, weights):
        # Ignore weights

        pixels = []
        for row in range(0, 8):
            for col in range(int(self.window), int(self.window)+self.WINDOW_WIDTH):
                if self.wall[row][col]:
                    pixels.append((self.max_value, 0, 0))
                else:
                    pixels.append((0, 0, 0))

        self.window += self.speed
        if self.window >= len(self.wall[0]) - self.WINDOW_WIDTH:
            self.window = 0.0

        return pixels
