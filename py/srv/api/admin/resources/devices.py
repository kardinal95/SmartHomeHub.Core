import uuid

from flask_restful import Resource, reqparse, abort

from py.srv.api.admin.models.devices import DeviceDTO
from py.srv.api.admin.models.endpoints import EndpointDTO, get_required_params
from py.srv.api.admin.operations.devices import get_all_devices, process_modifications
from py.srv.api.admin.operations.endpoints import get_all_endpoints, get_endpoint_parameters
from py.srv.api.exceptions import abort_on_exc, ApiOperationError
from py.srv.database import db_session


parser = reqparse.RequestParser()
parser.add_argument('mods',
                    help='This field cannot be blank',
                    type=dict,
                    required=True,
                    location='json')


class Devices(Resource):
    @abort_on_exc
    @db_session
    def get(self, session):
        devices = get_all_devices(session=session)
        return [DeviceDTO(x).as_json() for x in devices]

    @abort_on_exc
    @db_session
    def post(self, session):
        args = parser.parse_args()

        try:
            process_modifications(mods=args['mods'], session=session)
        except ApiOperationError as e:
            abort(400, message=e.as_json())
        return


class DevicesShort(Resource):
    @abort_on_exc
    @db_session
    def get(self, session):
        devices = get_all_devices(session=session)
        return [{
            'uuid': str(x.uuid),
            'name': x.name
        } for x in devices]