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
    ops = list()

    for item in mods:
        if item['name'] == "":
            raise ApiOperationError("add", "Name cannot be empty", item)
        if DriverInstanceMdl.get_instance_by_uuid(uuid=item['driver']['uuid'], session=session) is None:
            raise ApiOperationError("add", "Cannot find specified driver", item['driver'])
        ep = EndpointMdl(uuid=uuid.UUID(item['uuid']),
                         name=item['name'],
                         driver=DriverInstanceMdl.get_instance_by_uuid(uuid=uuid.UUID(item['driver']['uuid']),
                                                                       session=session))
        ep.driver_type = ep.driver.driver_type
        if ep.driver_type == DriverTypeEnum.mqtt:
            ep.mqtt_params = MqttParamsMdl()
            if "topic_read" not in item['parameters'].keys():
                raise ApiOperationError("add", "Missing required parameter: topic_read", item)
            ep.mqtt_params.topic_read = item['parameters']['topic_read']['value']
            if "topic_write" in item['parameters'].keys():
                ep.mqtt_params.topic_write = item['parameters']['topic_write']['value']
            if "type" not in item['parameters'].keys():
                raise ApiOperationError("add", "Missing required parameter: type", item)
            if MqttTypeMdl.get_by_name(name=item['parameters']['type']['value'],
                                       session=session) is None:
                raise ApiOperationError("add", "Cannot find specified mqtt type", item['parameters']['type']['value'])
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
                    raise ApiOperationError("add",
                                            f"Incorrect alarm severity: {item['parameters']['severity']['value']}",
                                            item)
            if "acl" not in item['parameters'].keys():
                ep.alarm_params.acl = 100
            else:
                try:
                    ep.alarm_params.acl = int(item['parameters']['acl']['value'])
                except ValueError:
                    raise ApiOperationError("add",
                                            f"Incorrect value for acl: {item['parameters']['acl']['value']}",
                                            item)
        elif ep.driver_type == DriverTypeEnum.setpoint:
            ep.setpoint_params = SetpointParamsMdl()
            if "name" not in item['parameters'].keys():
                raise ApiOperationError("add", "Missing required parameter: name", item)
            ep.name = item['parameters']['name']
            if "value" not in item['parameters'].keys():
                raise ApiOperationError("add", "Missing required parameter: value", item)
            ep.value = pickle.dumps(item['parameters']['value'])

        session.add(ep)
        ops.append(lambda: ServiceHub.retrieve(DriverSrv).get(ep.driver_uuid).add_endpoint(ep))
    session.flush()
    return ops


@db_session
def process_delete(mods, session):
    ops = list()

    for item in mods:
        ep = EndpointMdl.get_endpoint_by_uuid(uuid=uuid.UUID(item),
                                              session=session)
        try:
            session.delete(ep)
        except IntegrityError:
            raise ApiOperationError("delete",
                                    f"Cannot delete item in use with uuid: {item}")
        ops.append(lambda: ServiceHub.retrieve(DriverSrv).get(ep.driver_uuid).delete_endpoint(ep))
    session.flush()
    return ops


@db_session
def process_modifications(mods, session):
    ops = list()
    try:
        ops.extend(process_add(mods=mods['added'], session=session))
        ops.extend(process_delete(mods=mods['removed'], session=session))
    except ApiOperationError as e:
        session.rollback()
        raise e
    for item in ops:
        item()
    session.commit()
