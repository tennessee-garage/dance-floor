#!/usr/bin/env python

import argparse
import sys

from floor.controller import Test

import logging
LOG_FORMAT = "%(asctime)-15s | %(name)-12s (%(levelname)s): %(message)s"

logger = logging.getLogger("test-square")

def get_options():
    parser = argparse.ArgumentParser(description="Probe individual squares on the floor")
    parser.add_argument(
        "--floor_config", dest="floor_config", default=None, help="Use this floor configuration"
    )
    parser.add_argument(
        "--verbose", dest="verbose", action="store_true", help="Enable verbose logging"
    )
    parser.add_argument('square', type=int, help='The square to probe')
    parser.add_argument('red', type=int, help='The red value (0-1023)')
    parser.add_argument('green', type=int, help='The green value (0-1023)')
    parser.add_argument('blue', type=int, help='The blue value (0-1023)')
    return parser.parse_args()


def main():
    args = get_options()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format=LOG_FORMAT)

    logger.info(f"Probing square {args.square} with color (R:{args.red}, G:{args.green}, B:{args.blue})")

    leds = []
    for s in range(64):
        if s == args.square:
            leds.append((args.red, args.green, args.blue))
        else:
            leds.append((0, 0, 0))

    test = Test()
    test.run(leds)


if __name__ == "__main__":
    main()
