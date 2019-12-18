from py.srv.api.client.resources.devices import Device
from py.srv.api.client.resources.rooms import *
from py.srv.api.client.resources.users import *


def add_resources(api):
    api.add_resource(Rooms, '/api/client/rooms')
    api.add_resource(RoomDevices, '/api/client/rooms/<string:room_uuid>/devices')
    api.add_resource(UserLogin, '/api/client/auth/login')
    api.add_resource(TokenRefresh, '/api/client/auth/refresh')
    api.add_resource(UserLogoutRefresh, '/api/client/auth/logout/refresh')
    api.add_resource(UserLogoutAccess, '/api/client/auth/logout/access')
    api.add_resource(Device, '/api/client/devices/<string:device_uuid>')
    api.add_resource(SocketIOAccess, '/api/client/auth/socketio')