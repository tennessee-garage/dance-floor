"""A simple sprite-animation-style processor.

This module implements both the core Processor, and the Frame class
upon which it depends.

The basic idea is that the processor exists to show, in an infinte
loop, a series of Frames. Each Frame (as currently defined) consists
solely of a set of pixels plus a duration of the frame.

A fake timescale is invented, the "bip", which is the minimum unit of
display for a Frame. It's just a shorthand for "32nd note". By requiring
all Frames to declare their duration in terms of this virtual timescale,
animations of Frames become inherently BPM-sensitive (and
downbeat-sensitive), as the actual wall time of a "beat" is determined
dynamically at runtime through the `clocked` decorator.

Some potential future enhancements we could make:

* Allow frames to declare in/out transitions (e.g. fade in, fade out).
* Allow pixels to declare in/out transitions
* Allow pixels to declare durations independent of their frames
* Devise a more compact frame encoding, for use elsewhere (e.g. a GUI builder)
"""

import collections

from floor.processor.base import Base
from floor.processor.utils import clocked
from floor.util.color_utils import hex_to_rgb

# A "bip" is just a stupid term I made up for a 32nd note, because
# we're gonna do a lot in terms of 32nd notes and that's kinda hard
# to say.
BIPS_PER_WHOLE_NOTE = 32

# A "beat" is generally understood to be quarter note.
BEATS_PER_WHOLE_NOTE = 4

# Number of bips in a quarter note.
BIPS_PER_BEAT = BIPS_PER_WHOLE_NOTE / BEATS_PER_WHOLE_NOTE

# Maximum bips for a single frame. An arbitrary upper bound we can
# increase without consequence; serves only as a sanity check.
MAXIMUM_BIPS_PER_FRAME = 1024


class Frame:
    def __init__(self, pixels, duration_bips=BIPS_PER_WHOLE_NOTE):
        self.pixels = pixels
        self.duration_bips = duration_bips

    @classmethod
    def from_object(cls, obj):
        """Utility function to construct a `Frame` from a simple eg JSON object."""
        pixels = obj.get("pixels")
        duration_bips = obj.get("duration_bips")
        if pixels is None:
            raise ValueError("object is missing `pixels`")
        if duration_bips is None:
            raise ValueError("object is missing `duration_bips`")
        duration_bips = int(duration_bips)
        if duration_bips < 0 or duration_bips > MAXIMUM_BIPS_PER_FRAME:
            raise ValueError("duration_bips must be >= 0 and <= {}".format(MAXIMUM_BIPS_PER_FRAME))
        return cls(pixels=pixels, duration_bips=duration_bips)

    @classmethod
    def test_pattern_of_color(cls, color_hex, frame_duration_bips=BIPS_PER_BEAT):
        """Utility function to create a basic `Frame` of `color`."""
        pixel = hex_to_rgb(color_hex)
        black = hex_to_rgb("#000000")
        pattern1 = [pixel, black] * 32
        pattern2 = [black, pixel] * 32
        return [
            cls(pixels=pattern1, duration_bips=frame_duration_bips),
            cls(pixels=pattern2, duration_bips=frame_duration_bips),
        ]


DEFAULT_SPRITE_FRAMES = Frame.test_pattern_of_color("#00ff00")


class Spritely(Base):
    def __init__(self, frames=None, frames_json=None, **kwargs):
        super(Spritely, self).__init__(**kwargs)
        if not frames and frames_json:
            frames = []
            for f in frames_json:
                try:
                    frames.append(Frame.from_object(f))
                except ValueError:
                    pass
        if not frames:
            frames = DEFAULT_SPRITE_FRAMES

        self.frames = collections.deque(frames)
        self.current_frame = None
        self.bip_counter = 0

    @clocked(frames_per_beat=BIPS_PER_BEAT)
    def get_next_frame(self, context):
        if not self.frames:
            return None

        if self.bip_counter == 0:
            if self.current_frame is not None:
                self.frames.rotate()
            self.current_frame = self.frames[0]
            self.bip_counter = self.current_frame.duration_bips

        self.bip_counter -= 1
        return self.current_frame.pixels
