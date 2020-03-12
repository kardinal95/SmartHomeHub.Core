from py.srv.api.admin.resources.drivers import Drivers
from py.srv.api.admin.resources.meta import DriverTypes, DriverTypeParameters


def add_resources(api):
    api.add_resource(Drivers, '/api/admin/drivers')
    api.add_resource(DriverTypes, '/api/admin/meta/drivers/types')
    api.add_resource(DriverTypeParameters, '/api/admin/meta/drivers/types/<string:driver_type>')
