from flask_restful import Resource

from py.srv.api.admin.operations.rooms import get_all_rooms, get_room_devices
from py.srv.api.exceptions import abort_on_exc
from py.srv.database import db_session


class AdmRooms(Resource):
    @abort_on_exc
    @db_session
    def get(self, session):
        rooms = get_all_rooms(session=session)
        return {str(x.uuid): x.name for x in rooms}


class AdmRoomDevices(Resource):
    @abort_on_exc
    @db_session
    def get(self, room_uuid, session):
        devices = get_room_devices(uuid=room_uuid, session=session)
        return [str(x.uuid) for x in devices]