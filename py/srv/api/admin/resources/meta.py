from flask_restful import Resource

from py.srv.api.exceptions import abort_on_exc
from py.srv.database.models.driver import DriverTypeEnum


class DriverTypes(Resource):
    @abort_on_exc
    def get(self):
        return [x.name for x in list(DriverTypeEnum)]


class DriverTypeParameters(Resource):
    # TODO Change to config-based
    @abort_on_exc
    def get(self, driver_type):
        if driver_type == 'mqtt':
            return [
                {
                    'name': 'host',
                    'type': 'host',
                    'required': True,
                    'default': '127.0.0.1'
                },
                {
                    'name': 'port',
                    'type': 'number',
                    'required': True,
                    'default': 1883
                },
                {
                    'name': 'timeout',
                    'type': 'number',
                    'required': False,
                    'default': 60
                },
                {
                    'name': 'username',
                    'type': 'string',
                    'required': False,
                    'default': ''
                },
                {
                    'name': 'password',
                    'type': 'string',
                    'required': False,
                    'default': ''
                }
            ]
        return []
