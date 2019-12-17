import pickle

import redis
from dynaconf import settings
from loguru import logger

from py.srv.database import db_session


class RedisSrv:
    def __init__(self):
        self.redis = redis.Redis(host=settings.REDIS_HOST,
                                 port=settings.REDIS_PORT,
                                 db=settings.REDIS_DB_ID,
                                 decode_responses=False)
        self.watchers = list()

    def subscribe(self, func):
        self.watchers.append(func)

    @db_session
    def call_watchers(self, uuid, key_values, session):
        for item in self.watchers:
            item(uuid=uuid, key_values=key_values, session=session)

    def try_update(self, uuid, key, value):
        current = self.hget(uuid, key)
        if value != current:
            logger.debug('New value ({}: {} - {})'.format(uuid, key, value))
            self.hset(uuid, key, value)
            self.call_watchers(uuid=uuid, key_values={key: value})
            return True
        return False

    def hget(self, uuid, key):
        res = self.redis.hget(str(uuid), key)
        if res:
            return pickle.loads(res)

    def hgetall(self, uuid):
        res = self.redis.hgetall(str(uuid))
        if res:
            return {x.decode(): pickle.loads(res[x]) for x in res.keys()}

    def hset(self, uuid, key, value):
        res = self.redis.hset(str(uuid), key, pickle.dumps(value))
        return res
