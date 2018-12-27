import inspect
from floor.controller.midi.manager import MidiManager

BLANK_FRAME = [(0, 0, 0)] * 64


class clocked(object):
    """Utility decorator that interpolates a `get_next_frame` call according to bpm.

    You can think of this decorator as providing a TTL cache decorator for
    the method it decorates, the TTL being dynamically computed from
    `context.bpm`.

    Here is an example of a trivial processor which changes colors once per
    quarter note:

        COLORS = [RED, GREEN, BLUE]

        @clocked
        def get_next_frame(self, context):
            self.position += 1
            self.position %= len(COLORS)
            color = COLORS[self.position]
            return [color] * 64
    """
    def __init__(self, frames_per_beat=1):
        """Decorator constructor.

        Args
            frames_per_beat: Period for a single frame. The default value of `1`
                will hold `get_next_frame` for the duration of a single beat (quarter
                note). Any numeric value is allowed; `4` means a whole 4/4 measure, where
                `0.5` means an eighth note.
        """
        self.frames_per_beat = frames_per_beat
        self.current_frame = None
        self.last_time = None

    def __call__(self, fn, *args, **kwargs):
        def new_fn(*args, **kwargs):
            context = args[1]
            now = context.clock
            bpm = context.bpm or 120.0
            beats_per_second = 60.0/bpm
            frame_period = beats_per_second / float(self.frames_per_beat)

            # Too soon, return current frame.
            if self.last_time is not None and (now - self.last_time) < frame_period:
                return self.current_frame

            # Generate a new frame and return it.
            self.current_frame = fn(*args, **kwargs)
            self.last_time = now
            return self.current_frame
        return new_fn


class midictrl(object):
    """Decorator that registers the class method as a midi function callback.

    Only works on class methods as the decoration does not have access to the
    instance (which has not been created) when its invoked.

    Methods will be passed their class name, the context_value if provided (a constant
    that is tied to a MidiFunction, e.g. ranged_value_6 will have a context value of 6),
    and the value of the midi function itself. For note on/off this will be the note velocity,
    for control functions, this will be the value of that control.  In both cases, the value
    will be between 0 and 127.

    Example usage:

        @classmethod
        @midictrl(function=MidiFunctions.ranged_value_1)
        def adjust_speed(cls, context_value, value):
            cls.SPEED = value/127.0
    """
    def __init__(self, function):
        """Decorator constructor.

        Args
            function: A MidiFunctions function, e.g. MidiFunctions.ranged_value_1
        """
        self.function = function

    def __call__(self, fn, *args, **kwargs):
        stack = inspect.stack()
        processor_class = stack[1][3]
        midi_function = self.function

        MidiManager.register_processor_callback(processor_class, midi_function, fn)
        return fn
