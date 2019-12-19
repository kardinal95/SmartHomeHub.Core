from py.srv import ServiceHub
from py.srv.redis import RedisSrv


class SensorCommonEnt:
    @staticmethod
    def outputs(device):
        return ['value']

    def __init__(self, device):
        self.device = device


class SensorNumericEnt(SensorCommonEnt):
    def encode(self):
        redis = ServiceHub.retrieve(RedisSrv)
        return {
            'value': redis.hget(str(self.device.uuid), 'raw')
        }


class SensorBinaryEnt(SensorCommonEnt):
    def encode(self):
        redis = ServiceHub.retrieve(RedisSrv)
        v = redis.hget(str(self.device.uuid), 'raw')
        if v is None:
            return {
                'value': None
            }
        return {
            'value': bool(v)
        }