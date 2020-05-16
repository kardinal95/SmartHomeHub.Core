from py.srv.api.admin.resources.devices import Devices, DevicesShort
from py.srv.api.admin.resources.drivers import Drivers
from py.srv.api.admin.resources.endpoints import Endpoints, EndpointParameters, EndpointsParamsList
from py.srv.api.admin.resources.meta import DriverTypes, DriverTypeParameters
from py.srv.api.admin.resources.admrooms import AdmRooms, AdmRoomDevices


def add_resources(api):
    api.add_resource(Drivers, '/api/admin/drivers')
    api.add_resource(Endpoints, '/api/admin/endpoints')
    api.add_resource(EndpointsParamsList, '/api/admin/endpoints/paramlist')
    api.add_resource(EndpointParameters, '/api/admin/endpoints/<string:ep_uuid>/parameters')
    api.add_resource(Devices, '/api/admin/devices')
    api.add_resource(DevicesShort, '/api/admin/devices/short')
    api.add_resource(DriverTypes, '/api/admin/meta/drivers/types')
    api.add_resource(DriverTypeParameters, '/api/admin/meta/drivers/types/<string:driver_type>')
    api.add_resource(AdmRooms, '/api/admin/rooms')
    api.add_resource(AdmRoomDevices, '/api/admin/rooms/<string:room_uuid>/devices')
