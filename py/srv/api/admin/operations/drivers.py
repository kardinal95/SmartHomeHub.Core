from py.srv.database import db_session
from py.srv.database.models.driver import DriverInstanceMdl


@db_session
def get_drivers(session):
    return DriverInstanceMdl.get_all()
