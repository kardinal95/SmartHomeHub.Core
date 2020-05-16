from py.srv.database import db_session
from py.srv.database.models.room import RoomMdl


@db_session
def get_all_rooms(session):
    return RoomMdl.get_all_rooms(session=session)


@db_session
def get_room_devices(uuid, session):
    room = RoomMdl.get_room_with_uuid(uuid=uuid, session=session)
    devices = room.get_devices(session=session)
    return devices
