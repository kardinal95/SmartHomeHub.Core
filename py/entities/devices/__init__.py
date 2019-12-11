import enum

from py.entities.devices.rgb import RGBLightHexEnt
from py.entities.devices.sensors import SensorNumericEnt
from py.srv.database import db_session


class DeviceEntEnum(enum.Enum):
    SensorNumeric = enum.auto()
    SensorBinary = enum.auto()
    LightSwitch = enum.auto()
    Switch = enum.auto()
    RGBLightHex = enum.auto()
    Fan4Pos = enum.auto()


mapping = {
    DeviceEntEnum.SensorNumeric: SensorNumericEnt,
    DeviceEntEnum.RGBLightHex: RGBLightHexEnt
}


@db_session
def source_encode(session, device):
    return mapping[device.dev_type](device).encode()
