from flask_restful import reqparse, Resource

from py.srv.api.demo.models.rooms import DemoRoomDTO
from py.srv.api.demo.operations.rooms import *
from py.srv.api.exceptions import abort_on_exc
from py.srv.database import db_session

parser = reqparse.RequestParser()
parser.add_argument('rooms', type=list, location='json')


class DemoRooms(Resource):
    @abort_on_exc
    @db_session
    def get(self, session):
        return [DemoRoomDTO(x).as_json() for x in get_all_rooms(session=session)]

    @abort_on_exc
    @db_session
    def put(self, session):
        args = parser.parse_args()
        add_rooms(rooms=args['rooms'], session=session)

    @abort_on_exc
    @db_session
    def delete(self, session):
        args = parser.parse_args()
        delete_rooms(rooms=args['rooms'], session=session)
