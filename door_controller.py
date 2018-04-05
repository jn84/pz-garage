import argparse
import configparser
import door_handler as door
import paho.mqtt.client as mqtt

VERSION = '0.1a'

# Get the config file name
parser = argparse.ArgumentParser(description='File name of the config file used to launch the daemon.',
                                 epilog='Quantum states not supported.',
                                 prog='door_controller.py')
parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION)
parser.add_argument('--config', type=str, default='example.config',
                    help='Relative path to the config file for the daemon instance')

args = parser.parse_args()
