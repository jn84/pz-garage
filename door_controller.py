import argparse
import configuration_handler
import door_handler
import string
import sys
import paho.mqtt.client as mqtt

from os import path
from os import access
from os import R_OK
from configparser import Error as ConfigError

VERSION = '0.1a'

# Get the config file name
parser = argparse.ArgumentParser(description='Control a door. Probably a garage  door.',
                                 epilog='Quantum states not supported.',
                                 prog='door_controller.py')
parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + VERSION)
parser.add_argument('-c', '--config', type=str, default='example.config', dest='config_file',
                    help='File name of the config file used to launch the daemon.'
                         'If in the local directory (./) input only the file name.'
                         'If in another directory, input the full path.                 '
                         'The program MUST be run using a config file. If one is not '
                         'specified, the default example.config will be used. Make a '
                         'copy of example.config and modify the settings to suit your needs.')

# Get the config file name
args = parser.parse_args()

if not path.isfile(args.config_file) or not access(args.config_file, R_OK):
    print('The configuration file could not be found or read access was denied by the system.')
    sys.exit('Unable to access config file: ' + args.config_file)

# Parse the config file

try:
    config = configuration_handler.ConfigurationHandler(args.config_file)
except ConfigError as e:
    print(str(e))
    sys.exit("Error parsing the config file")
except TypeError as e:
    print(str(e))
    sys.exit("Error converting config variable to correct type. Check that all configuration variables "
             "are in the correct format.")

print(config.MQTT_CLIENT_ID)

