#!/usr/bin/env python

from floor.controller import Controller
from floor.controller import Playlist, PlaylistManager
from floor.controller.playlist import ProcessorNotFound
from floor.controller import Layout
from floor.controller.midi import MidiManager
from floor.server.server import run_server
from floor.processor import all_processors

import argparse
import importlib
import os
import sys
import logging
import re

LOG_FORMAT = '%(asctime)-15s | %(name)-12s (%(levelname)s): %(message)s'

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
PLAYLIST_DIR = os.path.join(CONFIG_DIR, 'playlists')
MIDI_MAPPING_DIR = os.path.join(CONFIG_DIR, 'midi_maps')

DEFAULT_PLAYLIST = os.path.join(PLAYLIST_DIR, 'default.json')
DEFAULT_DRIVERS = ['raspberry', 'devserver']
DEFAULT_USER_PLAYLISTS_DIR = PLAYLIST_DIR

logger = logging.getLogger('show')


def driver_to_classname(name):
    return re.sub(r'(?:^|_)([a-z])', lambda x: x.group(1).upper(), name)


def load_driver(driver_name, driver_args):
    try:
        module = importlib.import_module("floor.driver.{}".format(driver_name))
    except ImportError as e:
        logger.exception("Driver '{}' does not exist or could not be loaded: {}".format(driver_name, e))
        return None

    driver = getattr(module, driver_to_classname(driver_name))(driver_args)
    logger.info("Loaded driver '{}'".format(driver_name))
    return driver


def get_options():
    parser = argparse.ArgumentParser(description='Run the disco dance floor')
    parser.add_argument(
        '--driver',
        dest='driver_names',
        default=None,
        action='append',
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
        default=None,
        help='Load this playlist instead of the default {}'.format(DEFAULT_PLAYLIST)
    )
    parser.add_argument(
        '--user_playlists_dir',
        dest='user_playlists_dir',
        default=DEFAULT_USER_PLAYLISTS_DIR,
        help='Store and load user playlists here; blank to disable.'
    )
    parser.add_argument(
        '--floor_config',
        dest='floor_config',
        default=None,
        help='Use this floor configuration'
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
    parser.set_defaults(server_port=1977)
    return parser.parse_args()


def main():
    args = get_options()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format=LOG_FORMAT)

    layout = None
    if args.floor_config:
        layout = Layout(config_dir=CONFIG_DIR, config_name=args.floor_config)

    drivers = []
    driver_names = set(args.driver_names) or DEFAULT_DRIVERS

    for driver_name in args.driver_names:
        logger.info('Initializing driver "{}"'.format(driver_name))
        driver = load_driver(driver_name, {"config_dir": CONFIG_DIR})
        if not driver:
            logger.error('No driver, exiting.')
            sys.exit(1)
        driver.init_layout(layout)
        logger.info("Using layout: {}".format(driver.layout.name))
        drivers.append(driver)

    if args.playlist and args.processor_name:
        logger.error('Cannot provide both --playlist and --processor')
        sys.exit(1)

    if args.processor_name:
        try:
            playlist = Playlist.from_object({'name': args.processor_name})
        except ProcessorNotFound:
            logger.error('Processor "{}" unknown'.format(args.processor_name))
            sys.exit(1)
    elif args.playlist:
        playlist = Playlist.from_file(args.playlist, all_processors())
    else:
        playlist = Playlist.from_file(DEFAULT_PLAYLIST, all_processors())

    playlist_manager = PlaylistManager(playlist, user_playlists_dir=args.user_playlists_dir)
    show = Controller(drivers, playlist_manager)

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
        playlist_manager.initialize(all_processors())
        show.run_forever()
    except KeyboardInterrupt:
        logger.info('Got CTRL-C, quitting.')
        sys.exit(0)
    except Exception as e:
        logger.exception('Unexpected error, aborting: {}'.format(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
