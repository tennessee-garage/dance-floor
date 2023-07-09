import colorsys
import importlib
import os.path
from builtins import range

from floor.processor.base import Base
from floor.processor.constants import COLOR_MAXIMUM
from floor.processor.utils import clocked


class Message(Base):
    # The font to use
    DEFAULT_FONT = "synchronizer"
    # How far apart should the letters be
    KERNING = 1
    # Essentially the width of the dance floor
    WINDOW_WIDTH = 8
    # File with messages to display
    MESSAGE_FILE = "/tmp/messages.txt"
    # Default message to show if messages file is empty or missing
    DEFAULT_MESSAGE = "Burn baby burn, Disco Inferno"

    def __init__(self, **kwargs):
        super(Message, self).__init__(**kwargs)

        font_module = importlib.import_module("floor.processor.fonts.{}".format(self.DEFAULT_FONT))

        self.font = font_module.alpha()
        # The list of messages to scroll
        self.messages = []
        # The current message to scroll
        self.message_num = 0

        # The text color
        self.hue = 0.0
        self.saturation = 1.0
        self.value = 1.0

        # The color velocity
        self.hue_velocity = 0.01

        # The message converted to the font in an array
        self.wall = []
        # The current window position on the wall
        self.window = 0.0
        # How fast to scroll in pixels per frame
        self.speed = 0.33

        if "text" in kwargs:
            # Load a single message from the args
            self.messages.append(kwargs["text"])
        else:
            # Load a list of messages from the messages file
            self.load_messages()

        self.load_next_wall()

    def load_messages(self):
        if os.path.isfile(self.MESSAGE_FILE):
            try:
                self.load_messages_from_file()
            except IOError:
                self.load_default_message()
        else:
            self.load_default_message()

    def load_messages_from_file(self):
        msg_file = open(self.MESSAGE_FILE, "r")
        for line in msg_file:
            self.messages.append(line)
        msg_file.close()

    def load_default_message(self):
        self.messages = [self.DEFAULT_MESSAGE]

    def load_next_wall(self):
        self.wall = []
        self.window = 0.0
        mesg = self.messages[self.message_num]

        for row in range(0, 8):
            self.wall.append([])

            # Add blank space at the beginning so the text can scroll in from the side
            self.wall[row].extend([0] * self.WINDOW_WIDTH)

            # Add the characters for this row
            self.load_wall_row(mesg, row)

            # Add blank space at the end so the text can scroll off the side, minus the
            # kerning from the final letter
            self.wall[row].extend([0] * (self.WINDOW_WIDTH - self.KERNING))

        # Ready us for the next load
        self.message_num = (self.message_num + 1) % len(self.messages)

    def load_wall_row(self, mesg, row):
        for char in list(mesg):
            char_data = self.get_font_char(char)
            row_data = char_data[row]

            # Add this strip of the character to the wall
            self.wall[row].extend(row_data)
            # Add kerning
            self.wall[row].extend([0] * self.KERNING)

    def get_font_char(self, char):
        if char in self.font:
            return self.font[char]
        else:
            return self.font[" "]

    def shift_color(self):
        self.hue += self.hue_velocity
        if self.hue > 1.0:
            self.hue -= 1.0

    def current_rgb_tuple(self):
        rgb_float = colorsys.hsv_to_rgb(self.hue, self.saturation, self.value)
        rgb = list()

        rgb.append(int(rgb_float[0] * COLOR_MAXIMUM))
        rgb.append(int(rgb_float[1] * COLOR_MAXIMUM))
        rgb.append(int(rgb_float[2] * COLOR_MAXIMUM))

        return rgb

    @clocked(frames_per_second=24)
    def get_next_frame(self, context):
        pixels = []
        for row in range(0, 8):
            for col in range(int(self.window), int(self.window) + self.WINDOW_WIDTH):
                if self.wall[row][col]:
                    pixels.append(self.current_rgb_tuple())
                else:
                    pixels.append((0, 0, 0))

        self.shift_color()

        self.window += self.speed
        if self.window >= len(self.wall[0]) - self.WINDOW_WIDTH:
            self.load_next_wall()

        return pixels
