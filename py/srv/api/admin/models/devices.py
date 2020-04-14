import pickle

from py.srv.database import db_session
from py.srv.database.models.device import DeviceMdl, DeviceSourceMdl
from py.srv.database.models.endpoint import EndpointMdl
from py.srv.database.models.interface import InterfaceMdl
from py.srv.drivers.alarms.models import AlarmParamsMdl
from py.srv.drivers.mqtt.models import MqttParamsMdl, MqttTypeMdl
from py.srv.drivers.setpoints.models import SetpointParamsMdl
class InterfaceDTO:
    def __init__(self, interface: InterfaceMdl):
        self.read_acl = interface.read_acl
        self.write_acl = interface.write_acl

    def as_json(self):
        return {
            'read_acl': self.read_acl,
            'write_acl': self.write_acl
        }


class SourceDTO:
    def __init__(self, source: DeviceSourceMdl):
        self.ep_uuid = source.endpoint_uuid
        self.ep_param = source.endpoint_param
        self.device_param = source.device_param

    @classmethod
    def from_list(cls, items):
        return [cls(item) for item in items]

    def as_json(self):
        return {
            'ep_uuid': self.ep_uuid,
            'ep_param': self.ep_param,
            'device_param': self.device_param
        }


class DeviceDTO:
    def __init__(self, device: DeviceMdl):
        self.uuid = device.uuid
        self.name = device.name
        self.interface = InterfaceDTO(device.interface)
        self.sources = SourceDTO.from_list(device.sources)

    def as_json(self):
        return {
            'uuid': str(self.uuid),
            'name': self.name,
            'interface': self.interface.as_json(),
            'sources': [item.as_json() for item in self.sources]
        }
