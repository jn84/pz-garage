# Monitor state
# Trigger open/close

# State can change via external forces

import RPi.GPIO as GPIO
import time as time


class GarageDoor:
    """Garage door object"""  # __doc__ / docstring

    _valid_states = {0: 'Closed', 1: 'Open', 2: 'Intermediate'}

    # Whether the input should be high (True: button pull up) or (False: button pull down)
    #   when it is triggered
    _sensor_active_state_open = None
    _sensor_active_state_closed = None

    # BCM Pin to read sensor state
    _gpio_open_sensor_pin = None
    _gpio_closed_sensor_pin = None

    # Should be a value 0, 1, or 2 corresponding to _states
    current_state = -1

    def __init__(self, open_pin, closed_pin, open_active=True, closed_active=True):  # Constructor
        self._sensor_active_state_open = open_active
        self._sensor_active_state_closed = closed_active
        self._gpio_open_sensor_pin = open_pin
        self._gpio_closed_sensor_pin = closed_pin

        GPIO.setmode(GPIO.BCM)

        if self._sensor_active_state_open:
            GPIO.setup(self._gpio_open_sensor_pin, GPIO.RISING)
        else:
            GPIO.setup(self._gpio_open_sensor_pin, GPIO.FALLING)

        if self._sensor_active_state_closed:
            GPIO.setup(self._gpio_closed_sensor_pin, GPIO.RISING)
        else:
            GPIO.setup(self._gpio_closed_sensor_pin, GPIO.FALLING)

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

    # Start doing the thing
    def begin(self):



