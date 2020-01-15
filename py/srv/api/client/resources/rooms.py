import uuid

from flask_jwt_extended import *
from flask_restful import *

from py.srv.api.client.models.devices import DeviceDTO
from py.srv.api.client.models.rooms import RoomDTO
from py.srv.api.client.operations.devices import get_room_devices
from py.srv.api.client.operations.rooms import get_all_rooms
from py.srv.api.exceptions import abort_on_exc
from py.srv.database import db_session
from py.srv.database.models.user import UserMdl


class Rooms(Resource):
    @abort_on_exc
    @jwt_required
    @db_session
    def get(self, session):
        acl = UserMdl.get_user_with_username(username=get_jwt_identity(), session=session).acl
        rooms = get_all_rooms(session=session, acl=acl)

        return [RoomDTO(x).as_json() for x in rooms]


class RoomDevices(Resource):
    @abort_on_exc
    @jwt_required
    @db_session
    def get(self, room_uuid, session):
        acl = UserMdl.get_user_with_username(username=get_jwt_identity(), session=session).acl
        devices = get_room_devices(uuid=uuid.UUID(room_uuid), acl=acl, session=session)

        return [DeviceDTO(x, acl, x.get_key_values()).as_json() for x in devices]
