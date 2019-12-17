import enum

from py.entities.devices.rgb import RGBLightHexEnt
from py.entities.devices.sensors import SensorNumericEnt
from py.entities.devices.storage import StorageEnt


class DeviceEntEnum(enum.Enum):
    SensorNumeric = enum.auto()
    SensorBinary = enum.auto()
    LightSwitch = enum.auto()
    Switch = enum.auto()
    RGBLightHex = enum.auto()
    Fan4Pos = enum.auto()
    Storage = enum.auto()


mapping = {
    DeviceEntEnum.SensorNumeric: SensorNumericEnt,
    DeviceEntEnum.RGBLightHex: RGBLightHexEnt,
    DeviceEntEnum.Storage: StorageEnt
}


def source_encode(device):
    return mapping[device.dev_type](device).encode()


def source_decode(device):
    return mapping[device.dev_type](device).decode()


def outputs(device):
    return mapping[device.dev_type].outputs(device=device)