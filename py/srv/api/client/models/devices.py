class DeviceDTO:
    def __init__(self, device, acl, key_values):
        self.uuid = device.uuid
        self.name = device.name
        self.type = device.dev_type
        self.writable = device.interface.write_acl <= acl
        self.state = key_values

    def as_json(self):
        return {
            'uuid': str(self.uuid),
            'name': self.name,
            'type': self.type.name,
            'writable': self.writable,
            'state': self.state
        }