from py.entities.devices import DeviceEntEnum


class DemoDeviceSourceDTO:
    def __init__(self, info):
        self.endpoint = info['endpoint']
        self.ep_param = info['endpoint_parameter']
        self.device_param = info['device_parameter']

    def is_valid(self):
        return self.endpoint is not None\
               and self.endpoint != '' \
               and self.ep_param is not None \
               and self.ep_param != '' \
               and self.device_param is not None \
               and self.device_param != ''

    @classmethod
    def are_valid(cls, sources):
        for source in sources:
            if not source.is_valid():
                return False
        return True


class DemoDeviceDTO:
    def __init__(self, device):
        self.uuid = device.uuid
        self.name = device.name
        self.type = device.dev_type

    def as_json(self):
        return {
            'uuid': str(self.uuid),
            'name': self.name,
            'type': self.type.name
        }


class DemoDeviceInputDTO:
    def __init__(self, info):
        self.name = info['name']
        self.type = DeviceEntEnum[info['type']]
        self.rooms = info['rooms']
        self.sources = [DemoDeviceSourceDTO(x) for x in info['sources']]
        self.interface = info['interface']

    def is_valid(self):
        return self.name is not None \
               and self.name != '' \
               and DemoDeviceSourceDTO.are_valid(self.sources)