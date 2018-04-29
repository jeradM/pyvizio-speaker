import aiohttp
from aiohttp import TCPConnector

from .api_command import Command, InputListCommand, \
    InputCommand, VolumeCommand, KeyCommand, KeyCode, SystemCommand, \
    PowerCommand
from .api_response import Response, VizioResponseError


class Speaker:

    def __init__(self, host):
        self._inputs = None
        self._input = None
        self._volume = None
        self._power = None

        self._url_base = 'https://{}:9000'.format(host)

    async def start(self):
        await self.update_inputs()
        await self.update_current_input()
        await self.update_current_volume()
        await self.update_power_state()

    @property
    def inputs(self):
        if self._inputs is None:
            raise VizioResponseError('Input list empty. Was start() called?')
        return self._inputs

    @property
    def input(self):
        if self._input is None:
            raise VizioResponseError('No current input. Was start() called?')
        return self._input

    @property
    def volume(self):
        if self._volume is None:
            raise VizioResponseError('No current volume. Was start() called?')
        return self._volume

    @property
    def on(self):
        if self._power is None:
            raise VizioResponseError('Unknown state. Was start() called?')
        return self._power

    async def available(self):
        try:
            await self._status(SystemCommand())
            return True
        except VizioResponseError as err:
            print(err)

    async def update_inputs(self):
        resp = await self._status(InputListCommand())
        self._inputs = resp.items.as_list()
        return resp

    async def update_current_input(self):
        resp = await self._status(InputCommand())
        self._input = resp.items.first_value()
        return resp

    async def update_power_state(self):
        resp = await self._status(PowerCommand())
        self._power = resp.items.first_value() == 1

    async def update_current_volume(self):
        resp = await self._status(VolumeCommand())
        self._volume = resp.items.first_value()
        return resp

    async def set_input(self, target):
        if self._inputs is None:
            await self.update_inputs()
        if target not in self._inputs:
            return
        resp = await self._modify(InputCommand(target))
        self._input = target
        return resp.successful

    async def set_volume(self, volume):
        await self._modify(VolumeCommand(volume))
        await self.update_current_volume()

    async def volume_up(self):
        await self._key_command(KeyCommand(KeyCode.VOL_UP))
        await self.update_current_volume()

    async def volume_down(self):
        await self._key_command(KeyCommand(KeyCode.VOL_DOWN))
        await self.update_current_volume()

    async def mute(self):
        await self._key_command(KeyCommand(KeyCode.MUTE_ON))

    async def unmute(self):
        await self._key_command(KeyCommand(KeyCode.MUTE_OFF))

    async def mute_toggle(self):
        await self._key_command(KeyCommand(KeyCode.MUTE_TOGGLE))

    async def next_input(self):
        await self._key_command(KeyCommand(KeyCode.INPUT_NEXT))
        await self.update_current_input()

    async def power_on(self):
        if not self.on:
            await self.power_toggle()

    async def power_off(self):
        if self.on:
            await self.power_toggle()

    async def power_toggle(self):
        await self._key_command(KeyCommand(KeyCode.POWER_TOGGLE))
        await self.update_power_state()

    async def _status(self, command: Command):
        resp = await self._call(command, 'GET')
        return resp

    async def _modify(self, command: Command):
        if command.hash_val is None:
            await self._status(command)
        resp = await self._call(command, 'PUT')
        return resp

    async def _key_command(self, command):
        await self._call(command, 'PUT')

    async def _call(self, command: Command, method) -> Response:
        uri = '{}/{}'.format(self._url_base, command.endpoint.value)
        headers = {'Content-Type': 'application/json'}
        try:
            async with aiohttp.ClientSession(
                    headers=headers,
                    connector=TCPConnector(verify_ssl=False)) as session:
                if method == 'GET':
                    resp = await session.get(uri)
                elif method == 'PUT':
                    resp = await session.put(uri, json=command.request_obj)
                else:
                    raise aiohttp.ClientError('Unsupported Method')
                resp_data = await resp.json()
                resp_obj = command.handle_response(resp_data)
                if resp_obj.successful:
                    return resp_obj
                else:
                    raise VizioResponseError(resp_obj.status.status_msg)
        except aiohttp.ClientError as e:
            raise VizioResponseError(e.message)

