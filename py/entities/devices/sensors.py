from py.srv import ServiceHub
from py.srv.redis import RedisSrv


class SensorNumericEnt:
    def __init__(self, device):
        self.device = device

    def encode(self):
        redis = ServiceHub.retrieve(RedisSrv)
        return {
            'value': redis.hget(str(self.device.uuid), 'raw')
        }