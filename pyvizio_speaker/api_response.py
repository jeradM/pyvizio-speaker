class ResponseStatus:
    def __init__(self, status):
        self.status_msg = status.get("RESULT", "Vizio API Error")
        self.success = self.status_msg == 'SUCCESS'


class ResponseItem:
    def __init__(self, item):
        self.hash_val = item.get('HASHVAL')
        self.name = item.get('NAME')
        self.value = item.get('VALUE')


class ResponseItems:
    def __init__(self, items):
        self.items = []
        for item in items:
            self.items.append(ResponseItem(item))

    def as_list(self):
        return [item.name for item in self.items
                if item.name != 'Current Input']

    def first_value(self):
        if len(self.items) > 0:
            return self.items[0].value
        else:
            return None


class Response:
    def __init__(self, resp_obj):
        self.status = ResponseStatus(resp_obj.get('STATUS', {}))
        self.items = ResponseItems(resp_obj.get('ITEMS', []))
        self.uri = resp_obj.get('URI')

    @property
    def successful(self):
        return self.status.success

    @property
    def hash_val(self):
        if len(self.items.items) > 0:
            return self.items.items[0].hash_val
        else:
            return None


class VizioResponseError(Exception):
    pass
