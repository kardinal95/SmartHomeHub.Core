from py.srv.api.exceptions import ApiOperationError
from py.srv.database import db_session
from py.srv.database.models.device import DeviceMdl
from py.srv.database.models.room import RoomMdl

from uuid import UUID


@db_session
def get_all_rooms(session):
    return RoomMdl.get_all_rooms(session=session)


@db_session
def get_room_devices(uuid, session):
    room = RoomMdl.get_room_with_uuid(uuid=UUID(uuid), session=session)
    devices = room.get_devices(session=session)
    return devices


@db_session
def add_room(name, session):
    room = RoomMdl.get_room_with_name(name=name, session=session)
    if room is not None:
        raise ApiOperationError("Room with that name already exists", name)
    else:
        room = RoomMdl(name=name)
        session.add(room)
        session.commit()


@db_session
def delete_room(uuid, session):
    room = RoomMdl.get_room_with_uuid(uuid=uuid, session=session)
    if room is None:
        raise ApiOperationError("Room with this uuid is not found", uuid)
    else:
        session.delete(room)
        session.commit()


@db_session
def process_add(uuid, session, mods):
    room = RoomMdl.get_room_with_uuid(uuid=UUID(uuid), session=session)
    for item in mods:
        dev = DeviceMdl.get_device_with_uuid(uuid=UUID(item), session=session)
        room.devices.append(dev)
        session.add(room)
    session.flush()


@db_session
def process_delete(uuid, session, mods):
    room = RoomMdl.get_room_with_uuid(uuid=UUID(uuid), session=session)
    room.devices = [x for x in room.devices if str(x.uuid) not in mods]
    session.flush()


@db_session
def process_modifications(uuid, session, mods):
    try:
        process_add(uuid=uuid, mods=mods['added'], session=session)
        process_delete(uuid=uuid, mods=mods['removed'], session=session)
    except ApiOperationError as e:
        session.rollback()
        raise e
    session.commit()