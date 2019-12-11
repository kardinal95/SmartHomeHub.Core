from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from py.entities.devices import DeviceEntEnum
from py.srv import ServiceHub
from py.srv.database import db_session
from py.srv.database.models import DatabaseModel
from py.srv.redis import RedisSrv


class DeviceSourceMdl(DatabaseModel):
    __tablename__ = 'dev_sources'
    endpoint_uuid = Column(UUID(as_uuid=True), ForeignKey('endpoints.uuid'))
    endpoint_param = Column(String(64), nullable=False)
    device_uuid = Column(UUID(as_uuid=True), ForeignKey('devices.uuid'))
    device_param = Column(String(64), nullable=False)

    def try_update_ep(self, value):
        ServiceHub.retrieve(RedisSrv).try_update(self.device_uuid,
                                                 self.device_param,
                                                 value)

    @classmethod
    @db_session
    def get_by_endpoint_uuid(cls, uuid, session):
        return session.query(cls).filter(cls.endpoint_uuid == uuid).all()

    @classmethod
    @db_session
    def send_to_device(cls, ep_uuid, parameters, session):
        dss = session\
            .query(cls)\
            .filter(cls.endpoint_uuid == ep_uuid)\
            .filter(cls.device_param.in_(parameters.keys()))\
            .all()
        redis = ServiceHub.retrieve(RedisSrv)
        devices = list()
        for item in dss:
            if redis.try_update(str(item.device_uuid),
                                item.device_param,
                                parameters[item.endpoint_param]):
                devices.append(item.device_uuid)
        for item in set(devices):
            DeviceMdl.get_device_with_uuid(item).encode()


class DeviceParameterMdl(DatabaseModel):
    __tablename__ = 'dev_params'
    device_uuid = Column(UUID(as_uuid=True), ForeignKey('devices.uuid'))
    device_param = Column(String(64), nullable=False)
    value = Column(String(128), nullable=False)
    value_type = Column(String(64), nullable=False)


class DeviceMdl(DatabaseModel):
    __tablename__ = 'devices'
    name = Column(String(128), nullable=False)
    dev_type = Column(Enum(DeviceEntEnum))
    sources = relationship('DeviceSourceMdl',
                           cascade='all, delete-orphan',
                           backref=backref('device', uselist=False))
    parameters = relationship('DeviceParameterMdl',
                              cascade='all, delete-orphan',
                              backref=backref('device', uselist=False))

    @classmethod
    @db_session
    def get_all_devices(cls, session):
        return session.query(cls).all()

    @classmethod
    @db_session
    def get_device_with_uuid(cls, uuid, session):
        return session.query(cls).filter(cls.uuid == uuid).first()

    @db_session
    def encode(self):

        pass
