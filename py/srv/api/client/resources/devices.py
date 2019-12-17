import uuid

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from py.srv.api.client.operations.devices import set_state
from py.srv.api.exceptions import abort_on_exc
from py.srv.database import db_session
from py.srv.database.models.user import UserMdl


parser = reqparse.RequestParser()
parser.add_argument('parameters',
                    help='This field cannot be blank',
                    type=dict,
                    required=True,
                    location='json')


class Device(Resource):
    @abort_on_exc
    @jwt_required
    @db_session
    def patch(self, device_uuid, session):
        args = parser.parse_args()

        acl = UserMdl.get_user_with_username(username=get_jwt_identity(), session=session).acl
        set_state(uuid=uuid.UUID(device_uuid), parameters=args['parameters'], acl=acl, session=session)
