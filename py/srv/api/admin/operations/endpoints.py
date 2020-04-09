from py.srv.database import db_session
from py.srv.database.models.driver import DriverTypeEnum
from py.srv.database.models.endpoint import EndpointMdl


@db_session
def get_all_endpoints(session):
    return EndpointMdl.get_all(session=session)


@db_session
def get_endpoint_parameters(ep_uuid, session):
    ep = EndpointMdl.get_endpoint_by_uuid(uuid=ep_uuid, session=session)
    if ep.driver_type == DriverTypeEnum.mqtt:
        return ep.mqtt_params
    if ep.driver_type == DriverTypeEnum.setpoint:
        return ep.setpoint_params
    if ep.driver_type == DriverTypeEnum.alarm:
        return ep.alarm_params
