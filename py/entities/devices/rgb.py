from py.srv import ServiceHub
from py.srv.redis import RedisSrv


def _clamp(x):
    return max(0, min(x, 255))


def convert_to_hex(red, green, blue):
    return "#{0:02x}{1:02x}{2:02x}".format(_clamp(red), _clamp(green), _clamp(blue))


class RGBLightHexEnt:
    @staticmethod
    def keys():
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
