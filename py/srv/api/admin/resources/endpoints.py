from flask_restful import Resource

from py.srv.api.admin.models.endpoints import EndpointDTO
from py.srv.api.admin.operations.endpoints import get_all_endpoints
from py.srv.api.exceptions import abort_on_exc
from py.srv.database import db_session


class Endpoints(Resource):
    @abort_on_exc
    @db_session
    def get(self, session):
        endpoints = get_all_endpoints(session=session)
        return [EndpointDTO(x).as_json() for x in endpoints]
