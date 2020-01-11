import uuid

from flask_jwt_extended import *
from flask_restful import *
from flask_restful import reqparse

from py.srv.api.client.models.notifications import NotificationDTO
from py.srv.api.client.operations.notifications import get_notifications
from py.srv.api.exceptions import abort_on_exc
from py.srv.database import db_session
from py.srv.database.models.user import UserMdl

parser = reqparse.RequestParser()
parser.add_argument('limit', type=int, location='args', help='Amount of notifications to show')
parser.add_argument('skip', type=int, location='args', help='Amount of notifications to skip')


class Notifications(Resource):
    @abort_on_exc
    @jwt_required
    @db_session
    def get(self, session):
        acl = UserMdl.get_user_with_username(username=get_jwt_identity(), session=session).acl

        args = parser.parse_args()
        notifications = get_notifications(session=session, args=args, acl=acl)

        return [NotificationDTO(x).as_json() for x in notifications]