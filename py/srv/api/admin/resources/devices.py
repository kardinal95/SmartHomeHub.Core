import uuid

from flask_restful import Resource, reqparse, abort

from py.srv.api.admin.models.devices import DeviceDTO
from py.srv.api.admin.models.endpoints import EndpointDTO, get_required_params
from py.srv.api.admin.operations.devices import get_all_devices
from py.srv.api.admin.operations.endpoints import get_all_endpoints, get_endpoint_parameters, process_modifications
from py.srv.api.exceptions import abort_on_exc, ApiOperationError
from py.srv.database import db_session


class Devices(Resource):
    @abort_on_exc
    @db_session
    def get(self, session):
        devices = get_all_devices(session=session)
        return [DeviceDTO(x).as_json() for x in devices]
