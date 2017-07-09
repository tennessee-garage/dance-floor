from base import Base


def create():
    # Simply return a new instance of your class here
    return Test()


class Test(Base):

    SLOW_CYCLE = 30
    FAST_CYCLE = 2

    def __init__(self):
        super(Test, self).__init__()

        # helpful colors
        dark = (0,0,0)
        red = (self.DEFAULT_MAX_VALUE, 0, 0)
        blue = (0, self.DEFAULT_MAX_VALUE, 0)
        green = (0, 0, self.DEFAULT_MAX_VALUE)

        # define cycles
        self.cycles = []
        # full-floor cycles
        self.cycles.append({
            'floor': self.init_floor(red),
            'duration': self.SLOW_CYCLE
        })
        self.cycles.append({
            'floor': self.init_floor(blue),
            'duration': self.SLOW_CYCLE
        })
        self.cycles.append({
            'floor': self.init_floor(green),
            'duration': self.SLOW_CYCLE
        })

        # cycles for individual squares
        for c in ["red","blue","green"]:
            for i in range(0, (self.FLOOR_WIDTH * self.FLOOR_HEIGHT)):
                floor = self.init_floor(dark)
                floor[i] = eval(c)
                self.cycles.append({
                    'floor': floor,
                    'duration': self.FAST_CYCLE
                })

        self.current_cycle = 0
        self.countdown = self.cycles[0]['duration']



    def init_floor(self, initial_value):
        frame = []
        for x in range(0, (self.FLOOR_WIDTH * self.FLOOR_HEIGHT)):
            frame.append(initial_value)
        return frame

    def get_next_frame(self, weights):
        self.countdown -= 1
        if (self.countdown == 0):
            self.current_cycle += 1
            if (self.current_cycle > len(self.cycles) - 1):
                self.current_cycle = 0
            self.countdown = self.cycles[self.current_cycle]['duration']

        return self.cycles[self.current_cycle]['floor']
