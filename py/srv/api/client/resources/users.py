from flask_jwt_extended import *
from flask_restful import *
from flask_restful import reqparse

from py.srv.api.client.operations.users import revoke_token
from py.srv.api.exceptions import abort_on_exc
from py.srv.database import db_session
from py.srv.database.models.user import UserMdl

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)


class UserLogin(Resource):
    @abort_on_exc
    @db_session
    def post(self, session):
        data = parser.parse_args()
        user = UserMdl.get_user_with_username(username=data['username'], session=session)

        if user is None:
            abort(404, message='Incorrect user/password')

        if user.verify_password(data['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            abort(404, message='Incorrect user/password')


class TokenRefresh(Resource):
    @abort_on_exc
    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()
        access_token = create_access_token(identity=user)
        return {
            'access_token': access_token
        }


class UserLogoutRefresh(Resource):
    @abort_on_exc
    @jwt_refresh_token_required
    @db_session
    def post(self, session):
        jti = get_raw_jwt()['jti']
        revoke_token(jti=jti, session=session)


class UserLogoutAccess(Resource):
    @abort_on_exc
    @jwt_required
    @db_session
    def post(self, session):
        jti = get_raw_jwt()['jti']
        revoke_token(jti=jti, session=session)