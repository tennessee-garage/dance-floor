#!/usr/bin/env python

from floor.controller import Controller
from floor.controller import Playlist
from floor.controller import Layout
from floor.controller.midi import MidiManager
from floor.server.server import run_server

import argparse
import importlib
import os
import sys
import logging

LOG_FORMAT = '%(asctime)-15s | %(name)-12s (%(levelname)s): %(message)s'

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = os.path.join(SCRIPT_DIR, 'config')
PLAYLIST_DIR = os.path.join(CONFIG_DIR, 'playlists')
MIDI_MAPPING_DIR = os.path.join(CONFIG_DIR, 'midi_maps')
DEFAULT_PLAYLIST = os.path.join(PLAYLIST_DIR, 'default.json')
DEFAULT_FLOOR_CONFIG_FILE = os.path.join(SCRIPT_DIR, 'config/floor-layout.json')

logger = logging.getLogger('show')

def load_driver(driver_name, driver_args):
    try:
        module = importlib.import_module("floor.driver.{}".format(driver_name))
    except ImportError as e:
        logger.exception("Driver '{}' does not exist or could not be loaded".format(driver_name))
        return None

    driver = getattr(module, driver_name.title())(driver_args)
    logger.info("Loaded driver '{}' with max LED value {}".format(driver_name, driver.MAX_LED_VALUE))
    return driver


def get_options():
    parser = argparse.ArgumentParser(description='Run the disco dance floor')
    parser.add_argument(
        '--driver',
        dest='driver_name',
        default='raspberry',
        help='Sets the driver to use when writing LED data and reading weight data (default "raspberry")'
    )
    parser.add_argument(
        '--processor',
        dest='processor_name',
        default=None,
        help='Sets the LED processor to generate each frame of light data'
    )
    parser.add_argument(
        '--playlist',
        dest='playlist',
        default=DEFAULT_PLAYLIST,
        help='Load and run this playlist on start'
    )
    parser.add_argument(
        '--floor_config',
        dest='floor_config',
        default=DEFAULT_FLOOR_CONFIG_FILE,
        help='Use this floor configuration'
    )
    parser.add_argument(
        '--no-opc-input',
        dest='opc_input',
        action='store_false',
        help='Turn off keyboard input handling'
    )
    parser.add_argument(
        '--opc-input',
        dest='opc_input',
        action='store_true',
        help='Turn on keyboard input handling'
    )
    parser.add_argument(
        '--verbose',
        dest='verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--server_port',
        dest='server_port',
        type=int,
        help='Web server port; -1 to disable.'
    )
    parser.add_argument(
        '--midi_server_port',
        dest='midi_server_port',
        default=None,
        type=int,
        help='MIDI server port; disabled if unset.'
    )
    parser.add_argument(
        '--midi_mapping',
        dest='midi_mapping',
        default=None,
        help='Function mapping between a MIDI device and floor functions'
    )
    parser.set_defaults(opc_input=True, server_port=1977)
    return parser.parse_args()

def main():
    args = get_options()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format=LOG_FORMAT)

    driver = load_driver(args.driver_name, {
        "opc_input": args.opc_input,
        "layout": Layout(args.floor_config),
    })
    if not driver:
        logger.error('No driver, exiting.')
        sys.exit(1)

    playlist = Playlist(args.playlist, args.processor_name)
    show = Controller(driver, playlist)

    if args.midi_server_port:
        midi_manager = MidiManager(
            port=args.midi_server_port,
            controller=show,
        )
        if args.midi_mapping:
            midi_manager.load_default_midi_mapping(MIDI_MAPPING_DIR, args.midi_mapping)

        midi_manager.run_server()

    if args.server_port >= 0:
        run_server(show, port=args.server_port)

    try:
        show.run_forever()
    except KeyboardInterrupt:
        logger.info('Got CTRL-C, quitting.')
        sys.exit(0)
    except Exception as e:
        logger.exception('Unexpected error, aborting.')
        sys.exit(1)

if __name__ == '__main__':
    main()
