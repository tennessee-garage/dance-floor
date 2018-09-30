import datetime
import mock
from freezegun import freeze_time
from unittest import TestCase
from floor.processor.utils import clocked


class FakeProcessor:
    bpm = 120


class UtilsTestCase(TestCase):
    def test_clocked(self):
        wrapped_fn = mock.Mock()
        wrapped_fn.side_effect = ['a', 'b', 'c', 'd']
        fn = clocked()(wrapped_fn)

        with freeze_time() as frozen_datetime:
            # First call should call the underlying wrapped function.
            ret = fn(FakeProcessor)
            self.assertEqual('a', ret)
            self.assertEqual(1, wrapped_fn.call_count)

            # Any number of subsequent calls, without advancing time, will not
            # call the underlying wrapped function.
            for i in xrange(100):
                ret = fn(FakeProcessor)
                self.assertEqual('a', ret)
                self.assertEqual(1, wrapped_fn.call_count)

            # Since we are at 120 bpm, the cache will be invalidated ever 0.5 seconds,
            # so let's move time forward.
            frozen_datetime.tick(delta=datetime.timedelta(seconds=0.4))
            ret = fn(FakeProcessor)
            self.assertEqual('a', ret)
            self.assertEqual(1, wrapped_fn.call_count)
            frozen_datetime.tick(delta=datetime.timedelta(seconds=0.1))
            ret = fn(FakeProcessor)
            self.assertEqual('b', ret)
            self.assertEqual(2, wrapped_fn.call_count)

    def test_clocked_with_frames_per_beat(self):
        wrapped_fn = mock.Mock()
        wrapped_fn.side_effect = ['a', 'b', 'c', 'd']
        fn = clocked(frames_per_beat=4)(wrapped_fn)

        # With frames_per_beat=4 instead of the default 1, we expect a new call
        # to the wrapped function every 0.125 seconds instead of every 0.5.

        with freeze_time() as frozen_datetime:
            self.assertEqual('a', fn(FakeProcessor))
            self.assertEqual(1, wrapped_fn.call_count)

            frozen_datetime.tick(delta=datetime.timedelta(seconds=0.1))
            self.assertEqual('a', fn(FakeProcessor))
            self.assertEqual(1, wrapped_fn.call_count)

            frozen_datetime.tick(delta=datetime.timedelta(seconds=0.025))
            self.assertEqual('b', fn(FakeProcessor))
            self.assertEqual(2, wrapped_fn.call_count)

            frozen_datetime.tick(delta=datetime.timedelta(seconds=0.125))
            self.assertEqual('c', fn(FakeProcessor))
            self.assertEqual(3, wrapped_fn.call_count)

            frozen_datetime.tick(delta=datetime.timedelta(seconds=0.1))
            self.assertEqual('c', fn(FakeProcessor))
            self.assertEqual(3, wrapped_fn.call_count)

            frozen_datetime.tick(delta=datetime.timedelta(seconds=2))
            self.assertEqual('d', fn(FakeProcessor))
            self.assertEqual(4, wrapped_fn.call_count)
