from py.srv.api.demo.resources.devices import Devices
from py.srv.api.demo.resources.endpoints import Endpoints
from py.srv.api.demo.resources.demorooms import DemoRooms


def add_resources(api):
    api.add_resource(Endpoints, '/api/demo/endpoints')
    api.add_resource(DemoRooms, '/api/demo/rooms')
    api.add_resource(Devices, '/api/demo/devices')