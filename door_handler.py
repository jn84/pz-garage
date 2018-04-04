# Monitor state
# Trigger open/close

# State can change via external forces

import RPi.GPIO as GPIO
import time as time


class GarageDoor:
    """Garage door object"""  # __doc__ / docstring

    _valid_states = {0: 'Closed', 1: 'Open', 2: 'Intermediate'}

    # Whether the input should be high (True: button/switch pull up) or low (False: button/switch pull down)
    #   when it is triggered
    _sensor_active_state_open = True
    _sensor_active_state_closed = True

    # BCM pins to read sensor states
    _gpio_open_sensor_pin = -1
    _gpio_closed_sensor_pin = -1

    #BCM pin of door trigger relay
    _gpio_door_trigger_pin = -1

    # How long the relay stays closed when triggering the door to change state
    _door_trigger_active_delay = 0.1

    # Should be a value 0, 1, or 2 corresponding to _states
    current_state = -1

    def __init__(self, door_pin, open_pin, closed_pin, trigger_delay=0.1, open_active=True, closed_active=True):  # Constructor
        self._gpio_door_trigger_pin = door_pin
        self._sensor_active_state_open = open_active
        self._sensor_active_state_closed = closed_active
        self._door_trigger_active_delay = trigger_delay
        self._gpio_open_sensor_pin = open_pin
        self._gpio_closed_sensor_pin = closed_pin

        GPIO.setmode(GPIO.BCM)

        if self._sensor_active_state_open:
            GPIO.setup(self._gpio_open_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else:
            GPIO.setup(self._gpio_open_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        if self._sensor_active_state_closed:
            GPIO.setup(self._gpio_closed_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else:
            GPIO.setup(self._gpio_closed_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def toggle_state(self):
        # fire the relay trigger

    # Keep track of the current state and trigger an "event" when the state changes
    # Any subscribers will do what they need with the event information
    def get_states(self):
        # do state monitoring stuff


    def parse_states(self, states=(0,0)):
        # Set current state and return the value
        if states[0] is 0 and states[1] is 0:
            self.current_state = 2
        elif states[0] is 0 and states[1] is 1:
            self.current_state = 0
        elif states[0] is 1 and states[1] is 0:
            self.current_state = 1
        else:
            self.current_state = -1
            # error
            # should handle case where both open and closed states are active simultaneously (invalid state)
            # Maybe let subscribers handle invalid state
        return self.current_state




