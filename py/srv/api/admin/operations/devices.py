import pickle
import uuid

from sqlalchemy.exc import IntegrityError

from py.entities.devices import DeviceEntEnum
from py.srv import ServiceHub
from py.srv.api.exceptions import ApiOperationError
from py.srv.database import db_session
from py.srv.database.models.device import DeviceMdl, DeviceSourceMdl
from py.srv.database.models.driver import DriverTypeEnum, DriverInstanceMdl
from py.srv.database.models.endpoint import EndpointMdl
from py.srv.database.models.interface import InterfaceMdl
from py.srv.drivers import DriverSrv
from py.srv.drivers.alarms.models import AlarmParamsMdl, AlarmSeverityEnum
from py.srv.drivers.mqtt.models import MqttParamsMdl, MqttTypeMdl
from py.srv.drivers.setpoints.models import SetpointParamsMdl


@db_session
def get_all_devices(session):
    return DeviceMdl.get_all_devices(session=session)


@db_session
def process_add(mods, session):
    for item in mods:
        dev = DeviceMdl(uuid=uuid.UUID(item['uuid']))
        if item['name'] == "":
            raise ApiOperationError("Name cannot be empty", item['uuid'])
        dev.name = item['name']
        if item['type'] == "":
            raise ApiOperationError("Type cannot be empty", item['uuid'])
        try:
            dev.dev_type = DeviceEntEnum[item['type']]
        except KeyError:
            raise ApiOperationError("Incorrect device type", item['uuid'])
        if item['exported']:
            if item['interface'] is None:
                raise ApiOperationError("Interface parameters not specified", item['uuid'])
            dev.interface = InterfaceMdl()
            dev.interface.read_acl = item['interface']['read_acl']
            dev.interface.write_acl = item['interface']['write_acl']

        for param in item['sources'].keys():
            if item['sources'][param]['ep_param'] == "":
                raise ApiOperationError('Endpoint parameter not specified', item['uuid'])
            if item['sources'][param]['ep_uuid'] == "":
                raise ApiOperationError('Endpoint uuid not specified', item['uuid'])
            if EndpointMdl.get_endpoint_by_uuid(uuid=uuid.UUID(item['sources'][param]['ep_uuid']),
                                                session=session) is None:
                raise ApiOperationError('Endpoint with selected uuid not found', item['uuid'])
            link = DeviceSourceMdl()
            link.device_param = param
            link.device_uuid = dev.uuid
            link.endpoint_param = item['sources'][param]['ep_param']
            link.endpoint_uuid = uuid.UUID(item['sources'][param]['ep_uuid'])
            dev.sources.append(link)
        session.add(dev)
    session.flush()


@db_session
def process_delete(mods, session):
    for item in mods:
        dev = DeviceMdl.get_device_with_uuid(uuid=uuid.UUID(item),
                                             session=session)
        if dev is None:
            raise ApiOperationError("Cannot find specified device", item)
        try:
            session.delete(dev)
            session.flush()
        except IntegrityError:
            raise ApiOperationError(f"Cannot delete item: currently in use", item)


@db_session
def process_edit(mods, session):
    with session.no_autoflush:
        for item in mods:
            dev = DeviceMdl.get_device_with_uuid(uuid=uuid.UUID(item['uuid']),
                                                 session=session)
            if item['name'] == "":
                raise ApiOperationError("Name cannot be empty", item['uuid'])
            dev.name = item['name']
            if item['exported']:
                if item['interface'] is None:
                    raise ApiOperationError("Interface parameters not specified", item['uuid'])
                if dev.interface is None:
                    dev.interface = InterfaceMdl()
                dev.interface.read_acl = item['interface']['read_acl']
                dev.interface.write_acl = item['interface']['write_acl']
            else:
                dev.interface = None
            if item['type'] == "":
                raise ApiOperationError("Type cannot be empty", item['uuid'])
            try:
                ent = DeviceEntEnum[item['type']]
                if ent != dev.dev_type:
                    dev.dev_type = DeviceEntEnum[item['type']]
            except KeyError:
                raise ApiOperationError("Incorrect device type", item['uuid'])
            dev.sources = list()
            for param in item['sources'].keys():
                if item['sources'][param]['ep_param'] == "":
                    raise ApiOperationError('Endpoint parameter not specified', item['uuid'])
                if item['sources'][param]['ep_uuid'] == "":
                    raise ApiOperationError('Endpoint uuid not specified', item['uuid'])
                if EndpointMdl.get_endpoint_by_uuid(uuid=uuid.UUID(item['sources'][param]['ep_uuid']),
                                                    session=session) is None:
                    raise ApiOperationError('Endpoint with selected uuid not found', item['uuid'])
                link = DeviceSourceMdl()
                link.device_param = param
                link.device_uuid = dev.uuid
                link.endpoint_param = item['sources'][param]['ep_param']
                link.endpoint_uuid = uuid.UUID(item['sources'][param]['ep_uuid'])
                dev.sources.append(link)
    session.flush()


@db_session
def process_modifications(mods, session):
    try:
        process_add(mods=mods['added'], session=session)
        process_delete(mods=mods['removed'], session=session)
        process_edit(mods=mods['changed'], session=session)
    except ApiOperationError as e:
        session.rollback()
        raise e
    session.commit()