import datetime

from floor.processor.base import Base
from floor.processor.utils import clocked
from floor.processor.constants import COLOR_MAXIMUM


class Life(Base):

    BPM = 94

    def __init__(self, **kwargs):
        super(Life, self).__init__(**kwargs)

        # used to track floor state
        self.active_px = self.init_frame(False)

        # used to track when to update the lifecycle
        self.last_update = datetime.datetime.now()
        self.cycle_duration = 60000000 / self.BPM / 2

        # add a "blinker" organism to the floor
        on = [(1, 1), (1, 2), (1, 3)]
        for p in on:
            self.active_px[self.idx(p)] = True

    def init_frame(self, initial_value):
        frame = []
        for x in range(0, (self.FLOOR_WIDTH * self.FLOOR_HEIGHT)):
            frame.append(initial_value)
        return frame

    def conway_cycle_board(self, input_vals):
        output_vals = self.init_frame(False)
        for y in range(0, self.FLOOR_HEIGHT):
            for x in range(0, self.FLOOR_WIDTH):
                index = ((x * self.FLOOR_WIDTH) + y)
                output_vals[index] = self.conway_cycle_pixel(input_vals, x, y)
        return output_vals

    def conway_cycle_pixel(self, board, x, y):
        index = ((x * self.FLOOR_WIDTH) + y)
        output = board[index]
        neighbor_count = self.conway_count_neighbors(board, x, y)
        if board[index]:
            # pixel is currently active
            if neighbor_count < 2:
                # "Any live cell with fewer than two live neighbours dies,
                # as if caused by underpopulation."
                output = False
            elif neighbor_count > 3:
                # "Any live cell with more than three live neighbours dies,
                # as if by overpopulation."
                output = False
        else:
            # pixel is currently inactive
            if neighbor_count == 3:
                # "Any dead cell with exactly three live neighbours becomes a live cell,
                # as if by reproduction."
                output = True
        return output

    def conway_count_neighbors(self, board, x_in, y_in):
        left_bound = max(x_in - 1, 0)
        right_bound = min(x_in + 2, self.FLOOR_WIDTH)
        bottom_bound = max(y_in - 1, 0)
        top_bound = min(y_in + 2, self.FLOOR_HEIGHT)

        count = 0
        for x in range(left_bound, right_bound):
            for y in range(bottom_bound, top_bound):
                if board[self.idx((x, y))]:
                    if not ((x == x_in) and (y == y_in)):
                        count += 1
        return count

    @clocked(frames_per_second=24)
    def get_next_frame(self, context):
        weights = context.weights
        
        # update_active_px with lifecycle
        delta = datetime.datetime.now() - self.last_update
        if delta.microseconds > self.cycle_duration:
            self.last_update = datetime.datetime.now()
            self.active_px = self.conway_cycle_board(self.active_px)

        # update active_px from weights
        for y in range(0, self.FLOOR_HEIGHT):
            for x in range(0, self.FLOOR_WIDTH):
                index = self.idx((x, y))
                if weights[index]:
                    self.active_px[index] = not self.active_px[index]

        # render active_px
        dark = (0, 0, 0)
        bright = (COLOR_MAXIMUM, COLOR_MAXIMUM, COLOR_MAXIMUM)
        pixels = []
        for y in range(0, self.FLOOR_HEIGHT):
            for x in range(0, self.FLOOR_WIDTH):
                output = dark
                if self.active_px[self.idx((x, y))]:
                    output = bright
                pixels.append(output)

        return pixels


def main():
    life = Life()
    frame = life.init_frame(False)

    # conway_count_neighbors
    on = [(1, 1), (1, 3), (2, 2), (2, 3)]
    for p in on:
        frame[life.idx(p)] = True
    count = life.conway_count_neighbors(frame, 2, 2)
    assert (count == 3), "it counts neighbors correctly"


if __name__ == "__main__":
    main()
