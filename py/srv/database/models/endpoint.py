from sqlalchemy import *
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.orm import relationship, backref

from py.srv.database import db_session
from py.srv.database.models import DatabaseModel
from py.srv.database.models.driver import DriverTypeEnum


class EndpointMdl(DatabaseModel):
    __tablename__ = 'endpoints'
    name = Column(String(64), unique=True)
    driver_uuid = Column(UUID(as_uuid=True), ForeignKey('drivers.uuid'))
    driver_type = Column(Enum(DriverTypeEnum))
    driver = relationship('DriverInstanceMdl',
                          uselist=False,
                          backref=backref('endpoints', cascade='all, delete-orphan'))

    @classmethod
    @db_session
    def get_endpoint_by_uuid(cls, uuid, session):
        return session.query(cls).filter(cls.uuid == uuid).first()

    @classmethod
    @db_session
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    @db_session
    def get_endpoint_by_name(cls, name, session):
        return session.query(cls).filter(cls.name == name).first()