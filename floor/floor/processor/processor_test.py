from unittest import TestCase
from floor import processor
from freezegun import freeze_time
import time
import datetime


def test_run_all_processors():
    """Run each processor for 30 fake seconds."""
    # Note: This test uses a fancy `nosetests` feature to generate
    # N tests, one for each processor. Mostly this makes reporting
    # a little nicer when a test fails. More info here:
    # https://nose.readthedocs.io/en/latest/writing_tests.html#test-generators
    processors = processor.ALL_PROCESSORS
    fake_weights = [0] * 64
    num_frames = 30 * 30
    clock_time_per_frame = datetime.timedelta(seconds=1/30.0)

    def run_test(processor_name):
        cls = processor.ALL_PROCESSORS[processor_name]
        with freeze_time('Jan 1, 2001') as fake_time:
            now = time.time()
            instance = cls()
            instance.set_bpm(120, downbeat=now)
            for i in xrange(num_frames):
                instance.get_next_frame(fake_weights)
                fake_time.tick(delta=clock_time_per_frame)

    for processor_name in processor.ALL_PROCESSORS.keys():
        yield run_test, processor_name
