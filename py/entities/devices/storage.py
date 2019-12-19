from py.srv import ServiceHub
from py.srv.redis import RedisSrv


class StorageEnt:
    @staticmethod
    def outputs(device):
        redis = ServiceHub.retrieve(RedisSrv)
        params = redis.hgetall(str(device.uuid))
        return params.keys()

    def __init__(self, device):
        self.device = device

    def encode(self):
        redis = ServiceHub.retrieve(RedisSrv)
        params = redis.hgetall(str(self.device.uuid))
        return params

    def decode(self):
        return self.encode()
