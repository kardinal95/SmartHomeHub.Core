import pickle
import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from py.srv import ServiceHub
from py.srv.api.exceptions import SimpleException
from py.srv.database import db_session
from py.srv.database.models.driver import DriverTypeEnum, DriverInstanceMdl
from py.srv.database.models.endpoint import EndpointMdl
from py.srv.drivers import DriverSrv
from py.srv.drivers.alarms.models import AlarmParamsMdl, AlarmSeverityEnum
from py.srv.drivers.mqtt.models import MqttParamsMdl, MqttTypeMdl
from py.srv.drivers.setpoints.models import SetpointParamsMdl


@db_session
def get_all_endpoints(session):
    return EndpointMdl.get_all(session=session)


@db_session
def add_endpoints(endpoints, session):
    res = list()
    for num, item in enumerate(endpoints):
        try:
            endpoint = add_endpoint(item=item, session=session)
        except IntegrityError as e:
            raise SimpleException('Duplicate on #{} in sequence. Stopping'.format(num))
        driver = ServiceHub.retrieve(DriverSrv).get(endpoint.driver_uuid)
        driver.add_endpoint(endpoint)
        res.append(endpoint)
    session.commit()
    return res


@db_session
def add_endpoint(item, session):
    driver_uuid = DriverInstanceMdl.get_instance_by_comment(item['driver_comment']).uuid
    endpoint = EndpointMdl(driver_uuid=driver_uuid,
                           driver_type=DriverTypeEnum[item['driver_type']],
                           name=item['name'])
    if endpoint.driver_type == DriverTypeEnum.mqtt:
        endpoint.mqtt_params = MqttParamsMdl(type_uuid=MqttTypeMdl.get_by_name(item['params']['type']).uuid,
                                             topic_read=item['params']['topic_read'],
                                             topic_write=item['params']['topic_write'])
    if endpoint.driver_type == DriverTypeEnum.setpoint:
        for sub in item['params']['pairs']:
            endpoint.setpoint_params.append(SetpointParamsMdl(name=sub['name'],
                                                              value=pickle.dumps(sub['value'])))
    if endpoint.driver_type == DriverTypeEnum.alarm:
        endpoint.alarm_params = AlarmParamsMdl(msg_on=item['params']['msg_on'],
                                               msg_off=item['params']['msg_off'],
                                               severity=AlarmSeverityEnum[item['params']['severity']],
                                               acl=item['params']['acl'],
                                               triggered=False)
    session.add(endpoint)
    session.flush()
    return endpoint


@db_session
def delete_endpoints(endpoints, session):
    for num, item in enumerate(endpoints):
        try:
            endpoint = delete_endpoint(item=item, session=session)
        except UnmappedInstanceError as e:
            raise SimpleException('Item #{} not found. Stopping'.format(num))
        driver = ServiceHub.retrieve(DriverSrv).get(endpoint.driver_uuid)
        driver.delete_endpoint(endpoint)
    session.commit()


@db_session
def delete_endpoint(item, session):
    endpoint = EndpointMdl.get_endpoint_by_uuid(uuid=item, session=session)
    session.delete(endpoint)
    session.flush()
    return endpoint
