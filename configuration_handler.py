import configparser

from random import choice


class ConfigurationHandler:
    INSTANCE_NAME = None  # type: str
    MQTT_HOST = None  # type: str
    MQTT_PORT = None  # type: int
    MQTT_CLIENT_ID = None  # type: str
    MQTT_USE_AUTHENTICATION = None  # type: bool
    MQTT_USERNAME = None  # type: str
    MQTT_PASSWORD = None  # type: str
    MQTT_USE_SSL = None  # type: bool
    MQTT_PORT_SSL = None  # type: int
    MQTT_TOPIC_TOGGLE_DOOR_STATE = None  # type: str
    MQTT_TOPIC_REPORT_DOOR_STATE = None  # type: str
    DOOR_CONTROL_OUTPUT_PIN = None  # type: int
    DOOR_OPEN_SENSOR_INPUT_PIN = None  # type: int
    DOOR_CLOSED_SENSOR_INPUT_PIN = None  # type: int
    DOOR_CONTROL_OUTPUT_ACTIVE = None  # type: bool
    DOOR_CONTROL_OUTPUT_ACTIVE_DELAY = None  # type: bool
    DOOR_OPEN_SENSOR_INPUT_ACTIVE = None  # type: bool
    DOOR_CLOSED_SENSOR_INPUT_ACTIVE = None  # type: bool

    _hexdigits = '0123456789abcdef'

    def generate_client_id(self):
        self.MQTT_CLIENT_ID = 'door_' + ''.join(choice(self._hexdigits) for _ in range(32))

    # Config parsing helpers
    @staticmethod
    def bool_parse(str_value: str, var_name: str, default: bool) -> object:
        val = str.lower(str_value)
        if val == '':
            return default
        if val == 'true' or val == 'high' or val == '1':
            return True
        if val == 'false' or val == 'low' or val == '0':
            return False
        raise TypeError('Config value "' + str_value + '" is invalid for ' + var_name)

    @staticmethod
    def int_parse(str_value: str, var_name: str, can_be_none: bool) -> object:
        if (str_value == '' or str_value is None) and can_be_none:
            return None
        if (str_value == '' or str_value is None) and not can_be_none:
            raise ValueError("Config value cannot be empty for " + var_name)
        return int(str_value)

    @staticmethod
    def float_parse(str_value: str, var_name: str, can_be_none: bool) -> object:
        if (str_value == '' or str_value is None) and can_be_none:
            return None
        if (str_value == '' or str_value is None) and not can_be_none:
            raise ValueError("Config value cannot be empty for " + var_name)
        return float(str_value)

    @staticmethod
    def str_parse(str_value: str, var_name: str, can_be_none: bool) -> object:
        if str_value == '' and can_be_none:
            return None
        if str_value == '' and not can_be_none:
            raise TypeError('Config value is invalid for ' + var_name + ': value cannot be empty')
        return str(str_value)

    def get_port(self):
        if self.MQTT_USE_SSL:
            return self.MQTT_PORT_SSL
        return self.MQTT_PORT

    def __init__(self, config_file):

        config = configparser.ConfigParser()
        config.read(config_file)

        self.INSTANCE_NAME = self.\
            str_parse(config['General']['instance_name'],
                      'instance_name',
                      False)
        self.MQTT_HOST = self.\
            str_parse(config['MQTTBrokerConfig']['mqtt_host'],
                      'mqtt_host',
                      False)
        self.MQTT_PORT = self.\
            int_parse(config['MQTTBrokerConfig']['mqtt_port'],
                      'mqtt_port',
                      False)
        self.MQTT_CLIENT_ID = self.\
            str_parse(config['MQTTBrokerConfig']['mqtt_client_id'],
                      'mqtt_client_id',
                      True)
        self.MQTT_USE_AUTHENTICATION = self.\
            bool_parse(config['MQTTBrokerConfig']['mqtt_use_authentication'],
                       'mqtt_use_authentication',
                       False)
        self.MQTT_USERNAME = self.\
            str_parse(config['MQTTBrokerConfig']['mqtt_username'],
                      'mqtt_username',
                      not self.MQTT_USE_AUTHENTICATION)
        self.MQTT_PASSWORD = self.\
            str_parse(config['MQTTBrokerConfig']['mqtt_password'],
                      'mqtt_password',
                      not self.MQTT_USE_AUTHENTICATION)
        self.MQTT_USE_SSL = self.\
            bool_parse(config['MQTTBrokerConfig']['mqtt_use_ssl'],
                       'mqtt_use_ssl',
                       False)
        self.MQTT_PORT_SSL = self.\
            int_parse(config['MQTTBrokerConfig']['mqtt_port_ssl'],
                      'mqtt_port_ssl',
                      not self.MQTT_USE_SSL)
        self.MQTT_TOPIC_TOGGLE_DOOR_STATE = self.\
            str_parse(config['MQTTTopicConfig']['mqtt_topic_toggle_door_state'],
                      'mqtt_topic_toggle_door_state',
                      False)
        self.MQTT_TOPIC_REPORT_DOOR_STATE = self.\
            str_parse(config['MQTTTopicConfig']['mqtt_topic_report_door_state'],
                      'mqtt_topic_report_door_state',
                      False)
        self.DOOR_CONTROL_OUTPUT_PIN = self.\
            int_parse(config['GPIOConfig']['door_control_output_pin'],
                      'door_control_output_pin',
                      False)
        self.DOOR_OPEN_SENSOR_INPUT_PIN = self.\
            int_parse(config['GPIOConfig']['door_open_sensor_input_pin'],
                      'door_open_sensor_input_pin',
                      False)
        self.DOOR_CLOSED_SENSOR_INPUT_PIN = self.\
            int_parse(config['GPIOConfig']['door_closed_sensor_input_pin'],
                      'door_closed_sensor_input_pin',
                      False)
        self.DOOR_CONTROL_OUTPUT_ACTIVE = self.\
            bool_parse(config['GPIOActiveStates']['door_control_output_active_value'],
                       'door_control_output_active_value',
                       True)
        self.DOOR_CONTROL_OUTPUT_ACTIVE_DELAY = self.\
            float_parse(config['GPIOActiveStates']['door_control_output_active_delay'],
                        'door_control_output_active_delay',
                        False)
        self.DOOR_OPEN_SENSOR_INPUT_ACTIVE = self.\
            bool_parse(config['GPIOActiveStates']['door_open_sensor_input_active_value'],
                       'door_open_sensor_input_active_value',
                       True)
        self.DOOR_CLOSED_SENSOR_INPUT_ACTIVE = self.\
            bool_parse(config['GPIOActiveStates']['door_closed_sensor_active_value'],
                       'door_closed_sensor_active_value',
                       True)

        if self.MQTT_CLIENT_ID == '' or self.MQTT_CLIENT_ID is None:
            self.generate_client_id()
