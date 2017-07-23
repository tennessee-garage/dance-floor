from controller import Controller
from controller import Playlist
from server.server import run_server
import argparse
import os
import sys
import logging

LOG_FORMAT = '%(asctime)-15s | %(name)-12s (%(levelname)s): %(message)s'

def main():
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
    parser.set_defaults(opc_input=True, server_port=1977)
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format=LOG_FORMAT)

    config_dir = get_config_dir()
    playlist = Playlist(config_dir, args.processor_name)

    show = Controller(playlist)
    show.set_driver(args.driver_name, {
        "opc_input": args.opc_input
    })

    if args.server_port >= 0:
        run_server(show, port=args.server_port)

    try:
        show.run()
    except KeyboardInterrupt:
        sys.exit(0)


def get_config_dir():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return script_dir + "/config"

main()
