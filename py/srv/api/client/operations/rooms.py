from py.srv.api.client.operations.devices import get_room_devices
from py.srv.api.exceptions import IncorrectTargetException
from py.srv.database import db_session
from py.srv.database.models.room import RoomMdl


@db_session
def get_all_rooms(session, acl):
    rooms = RoomMdl.get_all_rooms(session=session)
    filtered = [x for x in rooms if len(get_room_devices(uuid=x.uuid, acl=acl, session=session)) > 0]
    return filtered


@db_session
def get_room(uuid, session):
    room = RoomMdl.get_room_with_uuid(uuid=uuid, session=session)
    if room is None:
        raise IncorrectTargetException(uuid, RoomMdl)
    return RoomMdl.get_room_with_uuid(uuid=uuid, session=session)