from .util import HashValsHolder, Endpoint, KeyCode
from .api_response import Response


class Command:
    def __init__(self, value=None):
        self._hash_vals = HashValsHolder.instance()
        self._value = value

    @property
    def hash_val(self):
        return self._hash_vals.get_hash_val(self.name)

    @property
    def endpoint(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError

    @property
    def request_obj(self):
        return {
            'REQUEST': 'MODIFY',
            'HASHVAL': self._hash_vals.get_hash_val(self.name),
            'VALUE': self._value
        }

    def handle_response(self, resp_obj):
        resp = Response(resp_obj)
        if resp.successful:
            self._hash_vals.set_hash_val(self.name, resp.hash_val)
        return resp


class InputListCommand(Command):
    @property
    def endpoint(self):
        return Endpoint.INPUTS

    @property
    def name(self):
        return 'inputs'

    @property
    def request_obj(self):
        raise NotImplementedError

    def handle_response(self, resp_obj):
        return Response(resp_obj)


class InputCommand(Command):
    @property
    def endpoint(self):
        return Endpoint.CURRENT_INPUT

    @property
    def name(self):
        return 'input'


class VolumeCommand(Command):
    @property
    def endpoint(self):
        return Endpoint.VOLUME

    @property
    def name(self):
        return 'volume'


class KeyCommand(Command):
    def __init__(self, *keys):
        super().__init__(keys)

    @property
    def endpoint(self):
        return Endpoint.KEY_COMMAND

    @property
    def name(self):
        return 'key_command'

    @property
    def request_obj(self):
        keylist = []
        for key in self._value:
            if not isinstance(key, KeyCode):
                continue
            keylist.append({
                'CODESET': key.value[0],
                'CODE': key.value[1],
                'ACTION': 'KEYPRESS'
            })
        return {'KEYLIST': keylist}


class PowerCommand(Command):
    @property
    def endpoint(self):
        return Endpoint.POWER

    @property
    def name(self):
        return 'power'

    def handle_response(self, resp_obj):
        return Response(resp_obj)


class SystemCommand(Command):
    @property
    def endpoint(self):
        return Endpoint.SYSTEM

    @property
    def name(self):
        return 'system'

    def handle_response(self, resp_obj):
        return Response(resp_obj)
