from py.srv import ServiceHub
from py.srv.redis import RedisSrv


class LightSwitchEnt:
    @staticmethod
    def outputs(device):
        return ['enabled']

    def __init__(self, device):
        self.device = device

    def encode(self):
        redis = ServiceHub.retrieve(RedisSrv)
        v = redis.hget(str(self.device.uuid), 'raw')
        if v is None:
            return {
                'enabled': None
            }
        return {
            'enabled': bool()
        }

    def decode(self):
        redis = ServiceHub.retrieve(RedisSrv)
        v = redis.hget(str(self.device.uuid), 'raw')
        if v is None:
            return {
                'raw': None
            }
        return {
            'raw': int()
        }