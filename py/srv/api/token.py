from sqlalchemy import *

from py.srv.database import db_session
from py.srv.database.models import DatabaseModel


class RevokedTokenMdl(DatabaseModel):
    __tablename__ = 'revoked_tokens'
    jti = Column(String(120))

    @classmethod
    @db_session
    def is_revoked_on(cls, jti, session):
        token = session.query(cls).filter(cls.jti == jti).first()
        if token is None:
            return False
        return True
