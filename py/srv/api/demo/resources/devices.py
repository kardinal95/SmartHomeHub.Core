from flask_restful import *
from flask_restful import reqparse

from py.srv.api.demo.models.devices import DemoDeviceDTO
from py.srv.api.demo.operations.devices import *
from py.srv.api.exceptions import abort_on_exc
from py.srv.database import db_session


parser = reqparse.RequestParser()
parser.add_argument('devices', type=list, location='json', required=True)


class Devices(Resource):
    @abort_on_exc
    @db_session
    def get(self, session):
        return [DemoDeviceDTO(x).as_json() for x in get_all_devices(session=session)]

    @abort_on_exc
    @db_session
    def put(self, session):
        args = parser.parse_args()
        return [DemoDeviceDTO(x).as_json() for x in add_devices(devices=args['devices'], session=session)]

    @abort_on_exc
    @db_session
    def delete(self, session):
        args = parser.parse_args()
        delete_devices(devices=args['devices'], session=session)
