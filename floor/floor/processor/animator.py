from base import Base
import importlib


class Animator(Base):

    DEFAULT_ANIMATION = "gods_eye"

    def __init__(self, **kwargs):
        super(Animator, self).__init__(**kwargs)

        animation = kwargs.get('animation', self.DEFAULT_ANIMATION)

        module = importlib.import_module("floor.processor.animations.{}".format(animation))
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
