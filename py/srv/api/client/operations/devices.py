from py.srv.api.client.operations.rooms import get_room
from py.srv.database import db_session


@db_session
def get_room_devices(uuid, acl, session):
    room = get_room(uuid=uuid, session=session)

    devices = [x for x in room.devices if x.interface is not None and x.interface.read_acl <= acl]
    return devices
