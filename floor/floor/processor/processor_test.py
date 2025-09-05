from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import time
from builtins import range
from unittest import TestCase

import pytest
from freezegun import freeze_time

from floor import processor
from floor.processor.base import Base as BaseProcessor
from floor.processor.base import RenderContext

TEST_FPS = 120
TEST_SECONDS = 30


@pytest.mark.parametrize("processor_name,processor_cls", list(processor.all_processors().items()))
def test_run_processor(processor_name, processor_cls):
    """Run each processor for 30 fake seconds."""
    fake_weights = [0] * 64
    num_frames = TEST_FPS * TEST_SECONDS
    clock_time_per_frame = datetime.timedelta(seconds=1 / TEST_FPS)

    with freeze_time("Jan 1, 2001") as fake_time:
        now = time.time()
        instance = processor_cls()
        for i in range(num_frames):
            context = RenderContext(
                clock=now,
                downbeat=0,
                weights=fake_weights,
                bpm=120.0,
                ranged_values=[0] * 4,
                switches=[False] * 4,
            )
            instance.get_next_frame(context)
            fake_time.tick(delta=clock_time_per_frame)


class ProcessorTest(TestCase):
    def test_all_processors_excludes_base(self):
        processors = processor.all_processors()
        self.assertTrue(BaseProcessor not in list(processors.values()))
