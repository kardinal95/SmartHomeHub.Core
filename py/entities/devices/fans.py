from py.srv import ServiceHub
from py.srv.redis import RedisSrv


class Fan4PosEnt:
    @staticmethod
    def outputs(device):
        return ['state']

    def __init__(self, device):
        self.device = device

    def encode(self):
        redis = ServiceHub.retrieve(RedisSrv)
        power = redis.hget(str(self.device.uuid), 'power')
        low = redis.hget(str(self.device.uuid), 'low')
        medium = redis.hget(str(self.device.uuid), 'medium')
        high = redis.hget(str(self.device.uuid), 'high')
        if any(x not in [0, 1] for x in [power, low, medium, high]):
            return {
                'state': None
            }
        if [power, low, medium, high] == [0, 0, 0, 0]:
            return {
                'state': 0
            }
        if [power, low, medium, high] == [1, 1, 0, 0]:
            return {
                'state': 1
            }
        if [power, low, medium, high] == [1, 0, 1, 0]:
            return {
                'state': 2
            }
        if [power, low, medium, high] == [1, 0, 0, 1]:
            return {
                'state': 3
            }
        return {
            'state': None
        }

    def decode(self):
        redis = ServiceHub.retrieve(RedisSrv)
        state = redis.hget(str(self.device.uuid), 'state')
        if state not in [0, 1, 2, 3]:
            return {
                'power': None,
                'low': None,
                'medium': None,
                'high': None
            }
        return {
            'power': int(state != 0),
            'low': int(state == 1),
            'medium': int(state == 2),
            'high': int(state == 3)
        }