from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import argparse
import logging
import timeit
import time

from floor.processor import all_processors
from floor.controller import Controller
from floor.controller.playlist import Playlist
from floor.driver.base import Base as BaseDriver


LOG_FORMAT = '%(levelname)s: %(message)s'
logger = logging.getLogger('benchmark')


class DummyDriver(BaseDriver):
    FAKE_WEIGHTS = [0] * 64

    def get_weights(self):
        return self.FAKE_WEIGHTS


def get_options():
    parser = argparse.ArgumentParser(description='Benchmark one or more processors.')

    parser.add_argument('processors',
        type=str,
        nargs='+',
        help='The name of the processor(s) to test, or "all" to test all.')

    parser.add_argument(
        '--iterations',
        dest='iterations',
        default=100000,
        type=int,
        help='How many iterations to run.',
    )

    parser.add_argument(
        '--verbose',
        dest='verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    parser.add_argument(
        '--disable_gc',
        dest='disable_gc',
        action='store_true',
        default=False,
        help='Whether to enable or disable garbage collection during benchmark.',
    )

    return parser.parse_args()


def benchmark_processor(name, processor, iterations, disable_gc):
    driver = DummyDriver({})
    playlist = Playlist(processor=processor)

    class FakeClock:
        def __init__(self):
            self.clock = 0

        def time(self):
            # Call time.time() so benchmark factors this in, even though we are ignoring
            # its value here in order to use our fake clock.
            time.time()
            return self.clock

        def sleep(self, amt):
            self.clock += amt

    clocksource = FakeClock()
    controller = Controller(driver=driver, playlist=playlist, clocksource=clocksource)

    if disable_gc:
        setup = ''
    else:
        setup = 'gc.enable()'

    def timed_function(controller=controller):
        controller.run_one_frame()

    timer = timeit.Timer(stmt=timed_function, setup=setup)
    total_time = timer.timeit(number=iterations)
    frames_per_second = round(iterations / total_time, 2)
    logger.info('Benchmark done! Took {} seconds'.format(total_time))
    logger.info('FPS={}'.format(frames_per_second))

    return frames_per_second


def print_results(results):
    print('Name              FPS')
    print('----------------  -----------')
    for name, fps in sorted(results.items(), key=lambda x: x[1]):
        print('{:16s}  {}'.format(name, int(fps)))


def run():
    args = get_options()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format=LOG_FORMAT)

    procs = all_processors()
    processors_to_test = {}

    for processor_name in args.processors:
        if processor_name == 'all':
            processors_to_test.update(procs)
        else:
            processor = procs.get(processor_name)
            if not processor:
                logging.error('Processor not found: {}'.format(args.processor))
                logging.error('Choices: {}'.format(', '.join(sorted(procs.keys()))))
                sys.exit(1)
            processors_to_test[processor_name] = processor

    results = {}
    names = sorted(processors_to_test.keys())
    for name in names:
        processor = processors_to_test[name]
        logger.info('Starting benchmark of {} with {} iterations ...'.format(name, args.iterations))
        result = benchmark_processor(name, processor, args.iterations, args.disable_gc)
        results[name] = result

    logger.info('Done!')
    print_results(results)


if __name__ == '__main__':
    run()
