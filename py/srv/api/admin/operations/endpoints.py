import pickle
import uuid

from sqlalchemy.exc import IntegrityError

from py.srv import ServiceHub
from py.srv.api.exceptions import ApiOperationError
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
def get_endpoint_parameters(ep_uuid, session):
    ep = EndpointMdl.get_endpoint_by_uuid(uuid=ep_uuid, session=session)
    if ep.driver_type == DriverTypeEnum.mqtt:
        return ep.mqtt_params
    if ep.driver_type == DriverTypeEnum.setpoint:
        return ep.setpoint_params
    if ep.driver_type == DriverTypeEnum.alarm:
        return ep.alarm_params


@db_session
def process_add(mods, session):
    eps = list()

    for item in mods:
        if item['name'] == "":
            raise ApiOperationError("Name cannot be empty", item['uuid'])
        if item['driver']['uuid'] == "":
            raise ApiOperationError("Driver cannot be empty", item['uuid'])
        if DriverInstanceMdl.get_instance_by_uuid(uuid=item['driver']['uuid'], session=session) is None:
            raise ApiOperationError("Cannot find specified driver", item['uuid'])
        ep = EndpointMdl(uuid=uuid.UUID(item['uuid']),
                         name=item['name'],
                         driver=DriverInstanceMdl.get_instance_by_uuid(uuid=uuid.UUID(item['driver']['uuid']),
                                                                       session=session))
        ep.driver_type = ep.driver.driver_type
        if ep.driver_type == DriverTypeEnum.mqtt:
            ep.mqtt_params = MqttParamsMdl()
            if "topic_read" not in item['parameters'].keys():
                raise ApiOperationError("Missing required parameter: topic_read", item['uuid'])
            if item['parameters']['topic_read']['value'] == "":
                raise ApiOperationError("Cannot subscribe on empty topics", item['uuid'])
            ep.mqtt_params.topic_read = item['parameters']['topic_read']['value']
            if "topic_write" in item['parameters'].keys():
                ep.mqtt_params.topic_write = item['parameters']['topic_write']['value']
            if "type" not in item['parameters'].keys():
                raise ApiOperationError("Missing required parameter: type", item['uuid'])
            if MqttTypeMdl.get_by_name(name=item['parameters']['type']['value'],
                                       session=session) is None:
                raise ApiOperationError("Cannot find specified mqtt type", item['uuid'])
            ep.mqtt_params.type = MqttTypeMdl.get_by_name(name=item['parameters']['type']['value'],
                                                          session=session)
        elif ep.driver_type == DriverTypeEnum.alarm:
            ep.alarm_params = AlarmParamsMdl(triggered=False)
            if "msg_on" in item['parameters'].keys():
                ep.alarm_params.topic_write = item['parameters']['msg_on']['value']
            if "msg_off" in item['parameters'].keys():
                ep.alarm_params.topic_write = item['parameters']['msg_off']['value']
            if "severity" not in item['parameters'].keys():
                ep.alarm_params.severity = AlarmSeverityEnum.Info
            else:
                try:
                    ep.alarm_params.severity = AlarmSeverityEnum[item['parameters']['severity']['value']]
                except KeyError:
                    raise ApiOperationError(f"Incorrect alarm severity: {item['parameters']['severity']['value']}",
                                            item['uuid'])
            if "acl" not in item['parameters'].keys():
                ep.alarm_params.acl = 100
            else:
                try:
                    ep.alarm_params.acl = int(item['parameters']['acl']['value'])
                except ValueError:
                    raise ApiOperationError(f"Incorrect value for acl: {item['parameters']['acl']['value']}",
                                            item['uuid'])
        elif ep.driver_type == DriverTypeEnum.setpoint:
            ep.setpoint_params = SetpointParamsMdl()
            if "name" not in item['parameters'].keys():
                raise ApiOperationError("Missing required parameter: name", item['uuid'])
            ep.name = item['parameters']['name']
            if "value" not in item['parameters'].keys():
                raise ApiOperationError("Missing required parameter: value", item['uuid'])
            ep.value = pickle.dumps(item['parameters']['value'])

        session.add(ep)
        eps.append(ep)
    session.flush()
    return eps


@db_session
def process_delete(mods, session):
    eps = list()

    for item in mods:
        ep = EndpointMdl.get_endpoint_by_uuid(uuid=uuid.UUID(item),
                                              session=session)
        try:
            session.delete(ep)
        except IntegrityError:
            raise ApiOperationError(f"Cannot delete item: currently in use", item['uuid'])
        eps.append(ep)
    session.flush()
    return eps


@db_session
def process_modifications(mods, session):
    eps = dict()
    try:
        eps['added'] = (process_add(mods=mods['added'], session=session))
        eps['removed'] = (process_delete(mods=mods['removed'], session=session))
    except ApiOperationError as e:
        session.rollback()
        raise e
    for item in eps['added']:
        ServiceHub.retrieve(DriverSrv).get(item.driver_uuid).add_endpoint(item)
    for item in eps['removed']:
        ServiceHub.retrieve(DriverSrv).get(item.driver_uuid).delete_endpoint(item)
    session.commit()
