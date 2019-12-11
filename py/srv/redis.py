import pickle

import redis
from dynaconf import settings
from loguru import logger


class RedisSrv:
    def __init__(self):
        self.redis = redis.Redis(host=settings.REDIS_HOST,
                                 port=settings.REDIS_PORT,
                                 db=settings.REDIS_DB_ID,
                                 decode_responses=False)
        self.watchers = list()

    def subscribe(self, func):
        self.watchers.append(func)

    def try_update(self, uuid, key, value):
        current = self.hget(uuid, key)
        if value != current:
            logger.debug('New value ({}: {} - {})'.format(uuid, key, value))
            self.hset(uuid, key, value)
            return True
        return False

    def hget(self, uuid, key):
        res = self.redis.hget(uuid, key)
        if res:
            return pickle.loads(res)

    def hset(self, uuid, key, value):
        res = self.redis.hset(uuid, key, pickle.dumps(value))
        return res
