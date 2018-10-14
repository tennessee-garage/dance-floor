from .base import Base
from .animator import Animator
from .chachacha import ChaChaCha
from .color_wash import ColorWash
from .electricity import Electricity
from .fire import Fire
from .fishies import Fishies
from .flash_bang import FlashBang
from .hyperspace import Hyperspace
from .kaleidoscope import Kaleidoscope
from .land_mines import LandMines
from .life import Life
from .message import Message
from .pulsar import Pulsar
from .random_decay import RandomDecay
from .raver_plaid import RaverPlaid
from .ripple import Ripple
from .ripple_pulse import RipplePulse
from .spiral import Spiral
from .stripes import Stripes
from .test_step import TestStep
from .test import Test
from .throbber import Throbber
from .zap import Zap

ALL_PROCESSORS = {
    'animator': Animator,
    'chachacha': ChaChaCha,
    'color_wash': ColorWash,
    'electricity': Electricity,
    'fire': Fire,
    'fishies': Fishies,
    'flash_bang': FlashBang,
    'hyperspace': Hyperspace,
    'kaleidoscope': Kaleidoscope,
    'land_mines': LandMines,
    'life': Life,
    'message': Message,
    'pulsar': Pulsar,
    'random_decay': RandomDecay,
    'raver_plaid': RaverPlaid,
    'ripple': Ripple,
    'ripple_pulse': RipplePulse,
    'spiral': Spiral,
    'stripes': Stripes,
    'test_step': TestStep,
    'test': Test,
    'throbber': Throbber,
    'zap': Zap,
}
