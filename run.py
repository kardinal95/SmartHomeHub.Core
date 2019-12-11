import sys

from dynaconf import *
from loguru import *
from sqlalchemy.orm import configure_mappers

from py.srv import ServiceHub
from py.srv.api import ApiSrv
from py.srv.database import DatabaseSrv, db_session
from py.srv.database.models.user import UserMdl
from py.srv.drivers import DriverSrv
from py.srv.redis import RedisSrv


def settings_validation():
    settings.validators.register(
        Validator('SQL_HOST', 'SQL_DBNAME', must_exist=True)
    )
    settings.validators.validate()


def configure():
    logger.remove()
    if settings.ENV_FOR_DYNACONF == 'production':
        logger.add('core.log', level='INFO', rotation='10 MB', backtrace=False, diagnose=False)
        logger.add(sys.stdout, level='INFO', colorize=True, backtrace=False, diagnose=False)
    if settings.ENV_FOR_DYNACONF == 'development':
        logger.add(sys.stdout, colorize=True, backtrace=True, diagnose=True)
        logger.add('debug.log', backtrace=True, diagnose=True)

    logger.debug('Running the program in {mode} environment...', mode=settings.ENV_FOR_DYNACONF)


def register_services():
    # TODO Move logging to services
    # Service loading
    ServiceHub.register(RedisSrv(), RedisSrv)
    ServiceHub.register(DatabaseSrv(), DatabaseSrv)
    # #ServiceHub.register(ExecutorSrv(), ExecutorSrv)

    # #ServiceHub.register(NotificationSrv(), NotificationSrv)
    # #ServiceHub.retrieve(NotificationSrv).add_target(
    # #    LoggingNotificationTarget(NotificationSeverityEnum.WARNING, prefix='ALARM'))

    ServiceHub.register(ApiSrv(), ApiSrv)

    # Exit if not connected
    if ServiceHub.retrieve(DatabaseSrv).connection is None:
        logger.critical('Cannot work without connection to database! Closing...')


@db_session
def demo_user(session):
    usr = UserMdl.get_user_with_username(username='demo', session=session)
    if usr is None:
        usr = UserMdl(username='demo', acl=100)
        usr.set_password('rf12ccb30')
        session.add(usr)
        session.commit()


if __name__ == '__main__':
    configure()
    try:
        settings_validation()
        register_services()
    except ValidationError as e:
        logger.exception(e)
    except KeyError as e:
        logger.exception(e)

    demo_user()
    configure_mappers()

    ServiceHub.register(DriverSrv(), DriverSrv)
    ServiceHub.retrieve(ApiSrv).run()
