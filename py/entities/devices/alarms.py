from py.srv.redis import RedisSrv
from py.srv import ServiceHub


class AlarmEnt:
    @staticmethod
    def outputs(device):
        return ['triggered']

    def __init__(self, device):
        self.device = device

    def encode(self):
        redis = ServiceHub.retrieve(RedisSrv)
        
        condition = redis.hget(str(self.device.uuid), 'condition')
        trigger = redis.hget(str(self.device.uuid), 'trigger')
        if trigger is None or condition is None:
            return {
                'triggered': False
            }
        return {
            'triggered': condition,
            'trigger': condition
        }