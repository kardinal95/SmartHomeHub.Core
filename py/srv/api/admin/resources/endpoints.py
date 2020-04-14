import uuid

from flask_restful import Resource, reqparse, abort

from py.srv.api.admin.models.endpoints import EndpointDTO, get_required_params
from py.srv.api.admin.operations.endpoints import get_all_endpoints, get_endpoint_parameters, process_modifications, \
    get_all_endpoint_params
from py.srv.api.exceptions import abort_on_exc, ApiOperationError
from py.srv.database import db_session


parser = reqparse.RequestParser()
parser.add_argument('mods',
                    help='This field cannot be blank',
                    type=dict,
                    required=True,
                    location='json')


class Endpoints(Resource):
    @abort_on_exc
    @db_session
    def get(self, session):
        endpoints = get_all_endpoints(session=session)
        return [EndpointDTO(x).as_json() for x in endpoints]

    @abort_on_exc
    @db_session
    def post(self, session):
        args = parser.parse_args()

        try:
            process_modifications(mods=args['mods'], session=session)
        except ApiOperationError as e:
            abort(400, message=e.as_json())
        return


class EndpointsParamsList(Resource):
    @abort_on_exc
    @db_session
    def get(self, session):
        return get_all_endpoint_params(session=session)


class EndpointParameters(Resource):
    @abort_on_exc
    @db_session
    def get(self, ep_uuid, session):
        params = get_endpoint_parameters(ep_uuid=uuid.UUID(ep_uuid), session=session)
        return get_required_params(params=params, session=session).as_json()