from controller import Controller
import argparse

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
    default='raver_plaid',
    help='Sets the LED processor to generate each frame of light data'
)
args = parser.parse_args()

show = Controller()
show.set_driver(args.driver_name)
show.set_processor(args.processor_name)

show.run()
