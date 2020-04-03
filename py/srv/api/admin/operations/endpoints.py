from py.srv.database import db_session
from py.srv.database.models.endpoint import EndpointMdl


@db_session
def get_all_endpoints(session):
    return EndpointMdl.get_all(session=session)
