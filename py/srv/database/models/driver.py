import enum
from pydoc import locate

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.orm import *

from py.srv.database import db_session
from py.srv.database.models import DatabaseModel


class DriverTypeEnum(enum.Enum):
    mqtt = enum.auto()
    setpoint = enum.auto()
    alarm = enum.auto()


class DriverInstanceMdl(DatabaseModel):
    __tablename__ = 'drivers'
    driver_type = Column(Enum(DriverTypeEnum))
    comment = Column(String(128), nullable=True)
    parameters = relationship("DriverParameterMdl", cascade='all, delete-orphan')

    @classmethod
    @db_session
    def get_instance_by_uuid(cls, uuid, session):
        return session.query(cls).filter(cls.uuid == uuid).first()

    @classmethod
    @db_session
    def get_instance_by_comment(cls, comment, session):
        return session.query(cls).filter(cls.comment == comment).first()


class DriverParameterMdl(DatabaseModel):
    __tablename__ = 'driver_parameters'
    driver_uuid = Column(UUID(as_uuid=True), ForeignKey('drivers.uuid'))
    param_name = Column(String(64))
    param_type = Column(String(64))
    param_value = Column(String(64))

    def get_as_pair(self):
        p_type = locate(self.param_type)
        return self.param_name, p_type(self.param_value)
