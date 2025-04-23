from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
from collections import OrderedDict
from glob import glob

from .base import Base, ProcessorRegistry


def _import_all():
    """Import all processors, to trigger registration."""
    pwd = os.path.dirname(__file__)
    for filename in glob(os.path.join(pwd, "*.py")):
        name, ext = os.path.splitext(os.path.basename(filename))
        __import__("floor.processor.{}".format(name), globals(), locals())


def all_processors():
    """Returns a dict of processor name -> processor class"""
    _import_all()
    return OrderedDict(sorted(ProcessorRegistry.ALL_PROCESSORS.items()))


__all__ = ["all_processors"]
