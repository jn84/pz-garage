import RPi.GPIO as GPIO
import time as time


class GarageDoor:
    """Garage door object"""  # __doc__ / docstring

    VERSION = '0.2a'

    STATE_CLOSED = 0
    STATE_OPEN = 1
    STATE_INTERMEDIATE = 2
    STATE_INVALID = -1

    # Creator of the object should assign a function to this variable in order to receive
    #   updates about sensor state changes
    # State change callback
    on_state_change = None

    # Whether the input should be high (True: button/switch pull up) or low (False: button/switch pull down)
    #   when it is triggered
    _sensor_active_state_open = True
    _sensor_active_state_closed = True

    # BCM pins to read sensor states
    _gpio_open_sensor_pin = -1
    _gpio_closed_sensor_pin = -1

    # BCM pin of door trigger relay
    _gpio_door_trigger_pin = -1
    # Default [OFF] state of the relay IO
    _gpio_door_trigger_active = True

    # How long the relay stays closed when triggering the door to change state nul
    _door_trigger_active_delay = 0.1

    # Should be a value 0, 1, 2, or -1
    _current_state = -1
    _previous_state = -1

    def __init__(self, door_pin, open_pin,
                 closed_pin, trigger_delay=0.1, door_active=True,
                 open_active=True, closed_active=True):
        self._gpio_door_trigger_pin = door_pin
        self._gpio_open_sensor_pin = open_pin
        self._gpio_closed_sensor_pin = closed_pin
        self._gpio_door_trigger_active = door_active
        self._sensor_active_state_open = open_active
        self._sensor_active_state_closed = closed_active
        self._door_trigger_active_delay = trigger_delay

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self._gpio_door_trigger_pin, GPIO.OUT, initial=int(not self._gpio_door_trigger_active))

        # Initialize state monitoring
        if self._sensor_active_state_open:
            GPIO.setup(self._gpio_open_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else:
            GPIO.setup(self._gpio_open_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        if self._sensor_active_state_closed:
            GPIO.setup(self._gpio_closed_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else:
            GPIO.setup(self._gpio_closed_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self._gpio_open_sensor_pin, GPIO.BOTH, callback=self.local_callback)
        GPIO.add_event_detect(self._gpio_closed_sensor_pin, GPIO.BOTH, callback=self.local_callback)

    def local_callback(self, channel):
        got_states = self.get_states()
        self.update_state(got_states)
        if self.on_state_change is not None:
            self.on_state_change(self._current_state, self._previous_state)

    def toggle_state(self):
        # If state is intermediate (probably moving) then ignore the toggle command
        # We want to just black hole the command so that the door doesn't trigger again
        if self._current_state is self.STATE_INTERMEDIATE:
            return None
        if self._current_state is self.STATE_INVALID:
            # Maybe do something if the state is invalid (notify to check hardware?)
            return None
        # Turn it on
        GPIO.output(self._gpio_door_trigger_pin, int(self._gpio_door_trigger_active))
        # Wait some time for door opener to catch up
        time.sleep(self._door_trigger_active_delay)
        # Turn it off
        GPIO.output(self._gpio_door_trigger_pin, int(not self._gpio_door_trigger_active))

    def get_states(self):
        open_sense_state = GPIO.input(self._gpio_open_sensor_pin)
        closed_sense_state = GPIO.input(self._gpio_closed_sensor_pin)
        return open_sense_state, closed_sense_state

    def update_state(self, states=(0, 0)):
        # Set current state and return the value
        self._previous_state = self._current_state
        if states[0] is int(not self._sensor_active_state_open) and\
                states[1] is int(not self._sensor_active_state_closed):
            self._current_state = 2
        elif states[0] is int(not self._sensor_active_state_open) and\
                states[1] is int(self._sensor_active_state_closed):
            self._current_state = 0
        elif states[0] is int(self._sensor_active_state_open) and\
                states[1] is int(not self._sensor_active_state_closed):
            self._current_state = 1
        else:
            self._current_state = -1
            # error
            # should handle case where both open and closed states are active simultaneously (invalid state)
            # Maybe let subscribers handle invalid state
        return self._current_state

    def get_current_state(self):
        states = self.get_states()
        self.update_state(states)
        return self._current_state

    def cleanup(self):
        GPIO.cleanup()

