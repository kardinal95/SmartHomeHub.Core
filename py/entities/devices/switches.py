from py.srv import ServiceHub
from py.srv.redis import RedisSrv


class SwitchEnt:
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
            'enabled': bool(v)
        }

    def decode(self):
        redis = ServiceHub.retrieve(RedisSrv)
        v = redis.hget(str(self.device.uuid), 'enabled')
        if v is None:
            return {
                'raw': None
            }
        return {
            'raw': int(v)
        }


class LightSwitchEnt(SwitchEnt):
    def __init__(self, device):
        super(LightSwitchEnt, self).__init__(device)
