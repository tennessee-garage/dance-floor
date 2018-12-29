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
    parser = argparse.ArgumentParser(description='Benchmark a processor.')

    parser.add_argument('processor',
        type=str,
        help='The name of the processor to test.')

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
    return parser.parse_args()


def run():
    args = get_options()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format=LOG_FORMAT)

    procs = all_processors()
    processor = procs.get(args.processor)
    if not processor:
        logging.error('Processor not found: {}'.format(args.processor))
        logging.error('Choices: {}'.format(', '.join(sorted(procs.keys()))))
        sys.exit(1)

    clock = 0
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
    
    def timed_function(controller=controller):
        controller.run_one_frame()

    timer = timeit.Timer(stmt=timed_function)
    logger.info('Starting benchmark of {} with {} iterations ...'.format(args.processor, args.iterations))
    total_time = timer.timeit(number=args.iterations)
    frames_per_second = round(args.iterations / total_time, 2)
    logger.info('Benchmark done! Took {} seconds'.format(total_time))
    logger.info('FPS={}'.format(frames_per_second))


if __name__ == '__main__':
    run()
