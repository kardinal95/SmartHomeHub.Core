import sqlalchemy as sql
from dynaconf import *
from loguru import logger
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import *

from py.srv import ServiceHub


def db_session(func):
    def wrapper(*args, **kwargs):
        if 'session' not in kwargs.keys():
            s = ServiceHub.retrieve(DatabaseSrv).session()
            kwargs['session'] = s
            res = func(*args, **kwargs)
            s.close()
            return res
        else:
            return func(*args, **kwargs)
    return wrapper


class DatabaseSrv:
    def __init__(self):
        self.engine = None
        self.connection = None
        self.session = None
        self.init_psql()

    def init_psql(self):
        settings.validators.register(
            Validator('psql_user', 'psql_pass', must_exist=True)
        )
        settings.validators.validate()

        self.engine = sql.create_engine('postgresql+psycopg2://{user}:{password}@{hostname}/{dbname}'.format(
            user=settings.PSQL_USER,
            password=settings.PSQL_PASS,
            hostname=settings.SQL_HOST,
            dbname=settings.SQL_DBNAME))

        try:
            self.connection = self.engine.connect()
            self.session = sessionmaker(bind=self.engine)
        except OperationalError as e:
            logger.exception(e)
            self.connection = None
