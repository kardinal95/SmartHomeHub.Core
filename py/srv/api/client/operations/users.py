from py.srv.api.token import RevokedTokenMdl
from py.srv.database import db_session
from py.srv.database.models.user import UserMdl


@db_session
def revoke_token(jti, session):
    session.add(RevokedTokenMdl(jti=jti))
    session.commit()


@db_session
def token_is_revoked(jti, session):
    return RevokedTokenMdl.is_revoked_on(jti=jti, session=session)


@db_session
def get_user_acl(username, session):
    return UserMdl.get_user_with_username(username=username, session=session).acl
