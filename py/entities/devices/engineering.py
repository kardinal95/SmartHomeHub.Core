from py.srv.redis import RedisSrv
from py.srv import ServiceHub


class InBorderTargetValueEnt:
    @staticmethod
    def check_emergency(value, target, tolerance):
        try:
            return value < target - tolerance or value > target + tolerance
        except TypeError:
            return False

    @staticmethod
    def outputs(device):
        return ['value', 'emergency']

    def __init__(self, device):
        self.device = device

    def encode(self):
        redis = ServiceHub.retrieve(RedisSrv)
        target = redis.hget(str(self.device.uuid), 'target')
        value = redis.hget(str(self.device.uuid), 'raw')
        tolerance = redis.hget(str(self.device.uuid), 'tolerance')
        if value is None:
            return {
                'value': None,
                'emergency': False
            }
        return {
            'value': value,
            'emergency': InBorderTargetValueEnt.check_emergency(value, target, tolerance)
        }