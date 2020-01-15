from py.srv import ServiceHub
from py.srv.api.client.operations.rooms import get_room
from py.srv.api.exceptions import *
from py.srv.database import db_session
from py.srv.database.models.device import DeviceMdl
from py.srv.database.models.room import RoomMdl
from py.srv.redis import RedisSrv


@db_session
def get_room_devices(uuid, acl, session):
    room = RoomMdl.get_room_with_uuid(uuid=uuid, session=session)

    devices = [x for x in room.devices if x.interface is not None and x.interface.read_acl <= acl]
    return devices


@db_session
def set_state(uuid, parameters, acl, session):
    device = DeviceMdl.get_device_with_uuid(uuid=uuid, session=session)
    if device is None:
        raise IncorrectTargetException(uuid, DeviceMdl)
    if device.interface.write_acl > acl:
        raise SimpleException('Not allowed for current user')
    if not all(item in parameters.keys() for item in device.get_key_values()):
        raise SimpleException('Incorrect parameter list')

    redis = ServiceHub.retrieve(RedisSrv)
    if any(redis.try_update(str(uuid), key, parameters[key]) for key in parameters.keys()):
        device.decode()
