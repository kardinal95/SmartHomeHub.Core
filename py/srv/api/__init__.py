from dynaconf import *
from flask import *
from flask_jwt_extended import *
from flask_restful import *

from py.srv.api.demo.resources.endpoints import Endpoints
from py.srv.api.token import RevokedTokenMdl


class ApiSrv:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)

        self.app.config['SECRET_KEY'] = settings.FLASK_SECRET_KEY
        self.app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
        self.app.config['JWT_BLACKLIST_ENABLED'] = True
        self.app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
        self.jwt = JWTManager(self.app)

        @self.jwt.token_in_blacklist_loader
        def check_if_token_in_blacklist_loader(decrypted_token):
            jti = decrypted_token['jti']
            return RevokedTokenMdl.is_revoked_on(jti=jti)

        self.add_resources()

    def add_resources(self):
        self.api.add_resource(Endpoints, '/api/demo/endpoints')

    def run(self):
        self.app.run(debug=False)