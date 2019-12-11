from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from py.srv.database import db_session
from py.srv.database.models import DatabaseModel


class DeviceRoomBinding(DatabaseModel):
    __tablename__ = 'device_room'
    device_uuid = Column(UUID(as_uuid=True), ForeignKey('devices.uuid'))
    room_uuid = Column(UUID(as_uuid=True), ForeignKey('rooms.uuid'))
    room = relationship('RoomMdl', uselist=False)
    device = relationship('DeviceMdl', uselist=False)

    @classmethod
    @db_session
    def get_devices_by_room_uuid(cls, uuid, session):
        binds = session.query(cls).filter(cls.room_uuid == uuid).all()
        return [x.device for x in binds]


class RoomMdl(DatabaseModel):
    __tablename__ = 'rooms'
    name = Column(String(64), nullable=False)

    @db_session
    def get_devices(self, session):
        return DeviceRoomBinding.get_devices_by_room_uuid(uuid=self.uuid, session=session)

    @classmethod
    @db_session
    def get_all_rooms(cls, session):
        return session.query(cls).all()

    @classmethod
    @db_session
    def get_room_with_uuid(cls, uuid, session):
        return session.query(cls).filter(cls.uuid == uuid).first()