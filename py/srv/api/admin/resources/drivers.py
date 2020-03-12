from flask_restful import Resource

from py.srv.api.admin.operations.drivers import get_drivers
from py.srv.api.exceptions import abort_on_exc
from py.srv.database import db_session


class Drivers(Resource):
    @abort_on_exc
    @db_session
    def get(self, session):
        drivers = get_drivers(session=session)
        return [x.as_json() for x in drivers]
