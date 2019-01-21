from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from freezegun import freeze_time
import time
import datetime
from unittest import TestCase

from floor import processor
from floor.processor.base import Base as BaseProcessor
from floor.processor.base import RenderContext


def test_run_all_processors():
    """Run each processor for 30 fake seconds."""
    # Note: This test uses a fancy `nosetests` feature to generate
    # N tests, one for each processor. Mostly this makes reporting
    # a little nicer when a test fails. More info here:
    # https://nose.readthedocs.io/en/latest/writing_tests.html#test-generators
    fake_weights = [0] * 64
    num_frames = 30 * 30
    clock_time_per_frame = datetime.timedelta(seconds=1/30.0)

    def run_test(processor_name, cls):
        with freeze_time('Jan 1, 2001') as fake_time:
            now = time.time()
            instance = cls()
            for i in xrange(num_frames):
                context = RenderContext(
                    clock=now,
                    downbeat=0,
                    weights=fake_weights,
                    bpm=120.0,
                )
                instance.get_next_frame(context)
                fake_time.tick(delta=clock_time_per_frame)

    processors = processor.all_processors()
    for processor_name, cls in processors.iteritems():
        yield run_test, processor_name, cls


class ProcessorTest(TestCase):
    def test_all_processors_excludes_base(self):
        processors = processor.all_processors()
        self.assert_(BaseProcessor not in processors.values())