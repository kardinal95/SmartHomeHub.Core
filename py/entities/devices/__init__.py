import enum


class DeviceEntEnum(enum.Enum):
    SensorNumeric = enum.auto()
    SensorBinary = enum.auto()
    LightSwitch = enum.auto()
    Switch = enum.auto()
    RGBLightHex = enum.auto()
    Fan4Pos = enum.auto()