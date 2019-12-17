from flask_restful import *
from flask_restful import reqparse

from py.srv.api.demo.models.endpoints import DemoEndpointDTO
from py.srv.api.demo.operations.endpoints import get_all_endpoints, add_endpoints, delete_endpoints
from py.srv.api.exceptions import abort_on_exc
from py.srv.database import db_session


parser = reqparse.RequestParser()
parser.add_argument('endpoints', type=list, location='json', required=True)


class Endpoints(Resource):
    @abort_on_exc
    @db_session
    def get(self, session):
        return [DemoEndpointDTO(x).as_json() for x in get_all_endpoints(session=session)]

    @abort_on_exc
    @db_session
    def put(self, session):
        args = parser.parse_args()
        return [DemoEndpointDTO(x).as_json() for x in add_endpoints(endpoints=args['endpoints'], session=session)]

    @abort_on_exc
    @db_session
    def delete(self, session):
        args = parser.parse_args()
        delete_endpoints(endpoints=args['endpoints'], session=session)
