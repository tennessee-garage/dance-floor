from base import Base
import importlib


def create():
    return Animator()


class Animator(Base):

    DEFAULT_ANIMATION = "Pac Man"

    def __init__(self):
        super(Animator, self).__init__()
        module = importlib.import_module("processor.animations.{}".format(self.DEFAULT_ANIMATION))
        self.animation = module.anim()
        self.floor_frame = 0
        self.animation_frame = 0
        self.fps_reduction = 2

    def get_next_frame(self, weights):
        # Ignore weights

        pixels = self.animation[self.animation_frame]

        if self.floor_frame % self.fps_reduction == 0:
            self.animation_frame = (self.animation_frame + 1) % len(self.animation)

        self.floor_frame = (self.floor_frame + 1) % 24

        return pixels
