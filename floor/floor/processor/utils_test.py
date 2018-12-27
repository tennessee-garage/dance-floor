import datetime
import mock
from unittest import TestCase
from floor.processor.utils import clocked
from floor.processor.base import RenderContext



class UtilsTestCase(TestCase):
    def test_clocked(self):
        wrapped_fn = mock.Mock()
        wrapped_fn.side_effect = ['a', 'b', 'c', 'd']
        fn = clocked()(wrapped_fn)

        processor = None
        clock = 0
        downbeat = 0
        weights = [0] * 64
        bpm = 120

        # First call should call the underlying wrapped function.
        ret = fn(processor, RenderContext(clock, downbeat, weights, bpm))
        self.assertEqual('a', ret)
        self.assertEqual(1, wrapped_fn.call_count)

        # Any number of subsequent calls, without advancing time, will not
        # call the underlying wrapped function.
        for i in xrange(100):
            ret = fn(processor, RenderContext(clock, downbeat, weights, bpm))
            self.assertEqual('a', ret)
            self.assertEqual(1, wrapped_fn.call_count)

        # Since we are at 120 bpm, the cache will be invalidated every 0.5 seconds,
        # so let's move time forward.
        clock += 0.4
        ret = fn(processor, RenderContext(clock, downbeat, weights, bpm))
        self.assertEqual('a', ret)
        self.assertEqual(1, wrapped_fn.call_count)
        clock += 0.1
        ret = fn(processor, RenderContext(clock, downbeat, weights, bpm))
        self.assertEqual('b', ret)
        self.assertEqual(2, wrapped_fn.call_count)

    def test_clocked_with_frames_per_beat(self):
        wrapped_fn = mock.Mock()
        wrapped_fn.side_effect = ['a', 'b', 'c', 'd']
        fn = clocked(frames_per_beat=4)(wrapped_fn)

        processor = None
        clock = 0
        downbeat = 0
        weights = [0] * 64
        bpm = 120
        
        # With frames_per_beat=4 instead of the default 1, we expect a new call
        # to the wrapped function every 0.125 seconds instead of every 0.5.

        self.assertEqual('a', fn(processor, RenderContext(clock, downbeat, weights, bpm)))
        self.assertEqual(1, wrapped_fn.call_count)

        clock += 0.1
        self.assertEqual('a', fn(processor, RenderContext(clock, downbeat, weights, bpm)))
        self.assertEqual(1, wrapped_fn.call_count)

        clock += 0.025
        self.assertEqual('b', fn(processor, RenderContext(clock, downbeat, weights, bpm)))
        self.assertEqual(2, wrapped_fn.call_count)

        clock += 0.125
        self.assertEqual('c', fn(processor, RenderContext(clock, downbeat, weights, bpm)))
        self.assertEqual(3, wrapped_fn.call_count)

        clock += 0.1
        self.assertEqual('c', fn(processor, RenderContext(clock, downbeat, weights, bpm)))
        self.assertEqual(3, wrapped_fn.call_count)

        clock += 2
        self.assertEqual('d', fn(processor, RenderContext(clock, downbeat, weights, bpm)))
        self.assertEqual(4, wrapped_fn.call_count)
