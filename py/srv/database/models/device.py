from itertools import groupby

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import *

from py.entities.devices import DeviceEntEnum, source_encode, outputs, source_decode
from py.srv import ServiceHub
from py.srv.database import db_session
from py.srv.database.models import DatabaseModel
from py.srv.database.models.endpoint import EndpointMdl
from py.srv.database.models.interface import InterfaceMdl # ORM
from py.srv.redis import RedisSrv


class DeviceSourceMdl(DatabaseModel):
    __tablename__ = 'dev_sources'
    endpoint_uuid = Column(UUID(as_uuid=True), ForeignKey('endpoints.uuid'))
    endpoint_param = Column(String(64), nullable=False)
    device_uuid = Column(UUID(as_uuid=True), ForeignKey('devices.uuid'))
    device_param = Column(String(64), nullable=False)

    @classmethod
    @db_session
    def get_by_endpoint_uuid(cls, uuid, session):
        return session.query(cls).filter(cls.endpoint_uuid == uuid).all()

    @classmethod
    @db_session
    def send_to_endpoint(cls, dev_uuid, key_values, session):
        from py.srv.drivers import DriverSrv
        dss = session \
            .query(cls) \
            .filter(cls.device_uuid == dev_uuid) \
            .filter(cls.device_param.in_(key_values.keys())) \
            .all()

        filtered = {}
        for key, group in groupby(dss, lambda x: x.endpoint_uuid):
            filtered[key] = {}
            for item in group:
                filtered[key][item.endpoint_param] = key_values[item.device_param]

        for key in filtered.keys():
            ep = EndpointMdl.get_endpoint_by_uuid(uuid=key, session=session)
            ServiceHub.retrieve(DriverSrv).get(ep.driver.uuid).data_to_ep(ep, filtered[key])
        print(filtered)

    @classmethod
    @db_session
    def send_to_device(cls, ep_uuid, parameters, session):
        dss = session\
            .query(cls)\
            .filter(cls.endpoint_uuid == ep_uuid)\
            .filter(cls.endpoint_param.in_(parameters.keys()))\
            .all()
        redis = ServiceHub.retrieve(RedisSrv)
        devices = list()
        for item in dss:
            if redis.try_update(str(item.device_uuid),
                                item.device_param,
                                parameters[item.endpoint_param]):
                devices.append(item.device_uuid)
        for item in set(devices):
            DeviceMdl.get_device_with_uuid(uuid=item, session=session).encode()


class DeviceMdl(DatabaseModel):
    __tablename__ = 'devices'
    name = Column(String(128), nullable=False, unique=True)
    dev_type = Column(Enum(DeviceEntEnum))
    interface = relationship('InterfaceMdl', uselist=False, cascade='all, delete-orphan')
    sources = relationship('DeviceSourceMdl',
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

    def encode(self):
        encoded = source_encode(self)
        redis = ServiceHub.retrieve(RedisSrv)
        for key in encoded.keys():
            redis.try_update(str(self.uuid), key, encoded[key])

    def decode(self):
        decoded = source_decode(self)
        redis = ServiceHub.retrieve(RedisSrv)
        for key in decoded.keys():
            redis.try_update(str(self.uuid), key, decoded[key])
        DeviceSourceMdl.send_to_endpoint(dev_uuid=self.uuid, key_values=decoded)

    def get_key_values(self):
        redis = ServiceHub.retrieve(RedisSrv)
        names = outputs(self)
        return {x: redis.hget(str(self.uuid), x) for x in names}

    def get_all_values(self):
        redis = ServiceHub.retrieve(RedisSrv)
        return redis.hgetall(str(self.uuid))