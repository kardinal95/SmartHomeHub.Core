from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from py.srv.api.demo.models.devices import DemoDeviceInputDTO
from py.srv.api.exceptions import SimpleException
from py.srv.database import db_session
from py.srv.database.models.device import DeviceMdl, DeviceSourceMdl
from py.srv.database.models.endpoint import EndpointMdl
from py.srv.database.models.interface import InterfaceMdl
from py.srv.database.models.room import RoomMdl, DeviceRoomBinding


@db_session
def get_all_devices(session):
    return DeviceMdl.get_all_devices(session=session)


@db_session
def delete_devices(devices, session):
    for num, item in enumerate(devices):
        try:
            delete_device(item=item, session=session)
        except UnmappedInstanceError as e:
            raise SimpleException('Item #{} not found. Stopping'.format(num))
    session.commit()


@db_session
def delete_device(item, session):
    device = DeviceMdl.get_device_with_uuid(uuid=item, session=session)
    session.delete(device)
    session.flush()
    return device


@db_session
def add_devices(devices, session):
    res = list()
    for num, item in enumerate(devices):
        try:
            res.append(add_device(item=item, session=session))
        except IntegrityError as e:
            raise SimpleException('Duplicate on #{} in sequence. Stopping'.format(num))
    session.commit()
    return res


@db_session
def add_device(item, session):
    model = DemoDeviceInputDTO(item)
    if not model.is_valid():
        raise SimpleException('Model is not valid!\n {}'.format(item))

    device = DeviceMdl(name=model.name,
                       dev_type=model.type)
    device.sources = list()
    device.room_binds = list()
    for source in model.sources:
        endpoint = EndpointMdl.get_endpoint_by_name(name=source.endpoint,
                                                    session=session)
        device.sources.append(DeviceSourceMdl(endpoint_uuid=endpoint.uuid,
                                              endpoint_param=source.ep_param,
                                              device_param=source.device_param))
    if model.interface['export'] is True:
        device.interface = InterfaceMdl(read_acl=model.interface['read_acl'],
                                        write_acl=model.interface['write_acl'])
    for room in model.rooms:
        mdl = RoomMdl.get_room_with_name(name=room, session=session)
        device.room_binds.append(DeviceRoomBinding(room=mdl))

    session.add(device)
    session.flush()
    return device
