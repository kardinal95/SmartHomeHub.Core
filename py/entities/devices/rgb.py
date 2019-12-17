from py.srv import ServiceHub
from py.srv.redis import RedisSrv


def _clamp(x):
    return max(0, min(x, 255))


def convert_to_hex(red, green, blue):
    return "#{0:02x}{1:02x}{2:02x}".format(_clamp(red), _clamp(green), _clamp(blue))


def convert_from_hex(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


class RGBLightHexEnt:
    @staticmethod
    def outputs(device):
        return ['color']

    def __init__(self, device):
        self.device = device

    def encode(self):
        redis = ServiceHub.retrieve(RedisSrv)
        red = redis.hget(str(self.device.uuid), 'red')
        green = redis.hget(str(self.device.uuid), 'green')
        blue = redis.hget(str(self.device.uuid), 'blue')
        return {
            'color': convert_to_hex(red, green, blue)
        }

    def decode(self):
        redis = ServiceHub.retrieve(RedisSrv)
        color = redis.hget(str(self.device.uuid), 'color')
        values = convert_from_hex(color)
        return {
            'red': values[0],
            'green': values[1],
            'blue': values[2]
        }