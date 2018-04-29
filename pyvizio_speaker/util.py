from enum import Enum


class Singleton:
    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


@Singleton
class HashValsHolder:
    def __init__(self):
        self.hash_vals = {}

    def get_hash_val(self, key):
        return self.hash_vals.get(key, None)

    def set_hash_val(self, key, value):
        self.hash_vals[key] = value


class Endpoint(Enum):
    CURRENT_INPUT = 'menu_native/dynamic/audio_settings/input/current_input'
    INPUTS = 'menu_native/dynamic/audio_settings/input'
    KEY_COMMAND = 'key_command/'
    POWER = 'state/device/power_mode'
    SYSTEM = 'menu_native/dynamic/audio_settings/system'
    VOLUME = 'menu_native/dynamic/audio_settings/audio/volume'


class KeyCode(Enum):
    VOL_DOWN = (5, 0)
    VOL_UP = (5, 1)
    MUTE_OFF = (5, 2)
    MUTE_ON = (5, 3)
    MUTE_TOGGLE = (5, 4)
    INPUT_NEXT = (7, 1)
    POWER_TOGGLE = (11, 2)


