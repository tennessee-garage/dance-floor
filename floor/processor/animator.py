from base import Base
import importlib


def create(args=None):
    return Animator(args)


class Animator(Base):

    DEFAULT_ANIMATION = "gods_eye"

    def __init__(self, args=None):
        super(Animator, self).__init__()

        if "animation" in args:
            animation = args["animation"]
        else:
            animation = self.DEFAULT_ANIMATION

        module = importlib.import_module("processor.animations.{}".format(animation))
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
