from .base import Base
from .animator import Animator
from .chachacha import ChaChaCha
from .color_wash import ColorWash
from .electricity import Electricity
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
    'stripes': Stripes,
    'test_step': TestStep,
    'test': Test,
    'throbber': Throbber,
    'zap': Zap,
}
