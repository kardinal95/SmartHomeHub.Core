from flask_restful import Resource

from py.srv.api.admin.models.endpoints import EndpointDTO, get_required_params
from py.srv.api.admin.operations.endpoints import get_all_endpoints, get_endpoint_parameters
from py.srv.api.exceptions import abort_on_exc
from py.srv.database import db_session


class Endpoints(Resource):
    @abort_on_exc
    @db_session
    def get(self, session):
        endpoints = get_all_endpoints(session=session)
        return [EndpointDTO(x).as_json() for x in endpoints]


class EndpointParameters(Resource):
    @abort_on_exc
    @db_session
    def get(self, ep_uuid, session):
        params = get_endpoint_parameters(ep_uuid=ep_uuid, session=session)
        return get_required_params(params=params, session=session).as_json()