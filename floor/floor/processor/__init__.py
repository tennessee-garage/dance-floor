from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os.path
from glob import glob
from collections import OrderedDict

from .base import ProcessorRegistry
from .base import Base


def _import_all():
    """Import all processors, to trigger registration."""
    pwd = os.path.dirname(__file__)
    for filename in glob(os.path.join(pwd, '*.py')):
        name, ext = os.path.splitext(os.path.basename(filename))
        __import__('floor.processor.{}'.format(name), globals(), locals())


def all_processors():
    """Returns a dict of processor name -> processor class"""
    _import_all()
    return OrderedDict(sorted(ProcessorRegistry.ALL_PROCESSORS.items()))


__all__ = ['all_processors']
