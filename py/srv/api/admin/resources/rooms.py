import uuid

from flask_restful import Resource, reqparse, abort

from py.srv.api.admin.operations.rooms import get_all_rooms, get_room_devices, process_modifications, add_room
from py.srv.api.exceptions import abort_on_exc, ApiOperationError
from py.srv.database import db_session


parser = reqparse.RequestParser()
parser.add_argument('mods',
                    help='This field cannot be blank',
                    type=dict,
                    required=True,
                    location='json')

parser2 = reqparse.RequestParser()
parser2.add_argument('name',
                     help='This field cannot be blank',
                     type=str,
                     required=True,
                     location='json')


class AdmRooms(Resource):
    @abort_on_exc
    @db_session
    def get(self, session):
        rooms = get_all_rooms(session=session)
        return [{
            'uuid': str(x.uuid),
            'name': x.name
        } for x in rooms]

    @abort_on_exc
    @db_session
    def post(self, session):
        args = parser2.parse_args()
        try:
            add_room(name=args['name'], session=session)
        except ApiOperationError as e:
            abort(400, message=e.as_json())
        return


class AdmRoomDevices(Resource):
    @abort_on_exc
    @db_session
    def get(self, room_uuid, session):
        devices = get_room_devices(room_uuid, session=session)
        return [str(x.uuid) for x in devices]

    @abort_on_exc
    @db_session
    def post(self, room_uuid, session):
        args = parser.parse_args()
        try:
            process_modifications(uuid=room_uuid, mods=args['mods'], session=session)
        except ApiOperationError as e:
            abort(400, message=e.as_json())
        return
