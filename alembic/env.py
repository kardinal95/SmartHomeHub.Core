import os
import sys
from logging.config import fileConfig

from dynaconf import settings
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.

config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
from py.srv.database.models import ModelBase
from py.srv.database.models.endpoint import *
from py.srv.database.models.device import *
from py.srv.database.models.driver import *
from py.srv.database.models.room import *
from py.srv.database.models.interface import *
from py.srv.database.models.trigger import *
from py.srv.database.models.scenario import *
from py.srv.database.models.instructions import *
from py.srv.database.models.condition import *
from py.srv.drivers.setpoints.models import *
from py.srv.drivers.mqtt.models import *
from py.srv.api.token import *
target_metadata = ModelBase.get_base().metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# return the current db url
def get_url():
    return 'postgresql+psycopg2://{user}:{password}@{hostname}/{dbname}'.format(
        user=settings.PSQL_USER, password=settings.PSQL_PASS,
        hostname=settings.SQL_HOST, dbname=settings.SQL_DBNAME)


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = create_engine(get_url())

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()