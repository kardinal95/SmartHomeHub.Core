from py.srv.database import db_session
from py.srv.database.models.device import DeviceSourceMdl, DeviceMdl


class LinkerSrv:
    @db_session
    def from_ep(self, uuid, pairs, session):
        devices = dict()

        for item in DeviceSourceMdl.get_by_endpoint_uuid(uuid=uuid, session=session):
            if item.device_uuid not in devices:
                devices[item.device_uuid] = dict()
            devices[item.device_uuid][item.device_param] = pairs[item.endpoint_param]

        for item in devices.keys():
            device = DeviceMdl.get_device_with_uuid(uuid=item, session=session)
            device.write_ep(devices[item])