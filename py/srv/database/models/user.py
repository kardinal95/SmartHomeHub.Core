import hashlib
import os

from sqlalchemy import *

from py.srv.database import db_session
from py.srv.database.models import DatabaseModel


def _make_salt():
    return os.urandom(32)


class UserMdl(DatabaseModel):
    __tablename__ = 'users'
    username = Column(String(64), unique=True)
    passhash = Column(Binary(32), nullable=False)
    salt = Column(Binary(32), nullable=False)
    acl = Column(Integer)

    @classmethod
    @db_session
    def get_user_with_username(cls, username, session):
        return session.query(cls).filter(cls.username == username).first()

    def set_password(self, password, salt=None):
        if salt is None:
            salt = _make_salt()
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )

        self.salt = salt
        self.passhash = key

    def verify_password(self, password):
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            self.salt,
            100000
        )
        if key == self.passhash:
            return True
        return False
