
BLANK_FRAME = [(0, 0, 0)] * 64


class clocked(object):
    """Utility decorator that interpolates a `get_next_frame` call according to bpm or time. 

    You can think of this decorator as providing a TTL cache decorator for
    the method it decorates, the TTL being dynamically computed from
    `context.bpm`.

    Here is an example of a trivial processor which changes colors once per
    quarter note:

        COLORS = [RED, GREEN, BLUE]

        @clocked(frames_per_beat=1)
        def get_next_frame(self, context):
            self.position += 1
            self.position %= len(COLORS)
            color = COLORS[self.position]
            return [color] * 64
    """
    def __init__(self, frames_per_beat=None, frames_per_second=None):
        """Decorator constructor.

        Args
            frames_per_beat: Period for a single frame, based on bpm. For example, a value of `1`
                will hold `get_next_frame` for the duration of a single beat (quarter
                note). Any numeric value is allowed; `4` means a whole 4/4 measure, where
                `0.5` means an eighth note.
            frames_per_second: Period for a single frame, in clock time. For example, a value
                of `30` will hold `get_next_frame` for the duration of (1/30.0) seconds, or roughly
                33ms.
        """
        if frames_per_beat is None and frames_per_second is None:
            raise ValueError('Must provide frames_per_beat and/or frames_per_second')
        self.frames_per_beat = frames_per_beat
        self.frames_per_second = frames_per_second
        self.current_frame = None
        self.next_time = None

    def __call__(self, fn, *args, **kwargs):
        def new_fn(*args, **kwargs):
            context = args[1]
            now = context.clock

            # Too soon, return current frame.
            if self.current_frame and self.next_time and now < self.next_time:
                return self.current_frame

            bps_deadline = None
            if self.frames_per_beat:
                bpm = context.bpm or 120.0
                beats_per_second = 60.0/bpm
                bps_frame_period = beats_per_second / float(self.frames_per_beat)
                bps_deadline = now + bps_frame_period

            fps_deadline = None
            if self.frames_per_second:
                fps_frame_period = 1.0 / self.frames_per_second
                fps_deadline = now + fps_frame_period
            
            if bps_deadline is not None and fps_deadline is not None:
                next_time = min(bps_deadline, fps_deadline)
            elif bps_deadline is not None:
                next_time = bps_deadline
            else:
                next_time = fps_deadline

            self.next_time = next_time

            # Generate a new frame and return it.
            self.current_frame = fn(*args, **kwargs)
            return self.current_frame
        return new_fn
