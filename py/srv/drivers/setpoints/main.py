import pickle

from loguru import *

from py.srv.database import db_session
from py.srv.database.models.device import DeviceSourceMdl
from py.srv.database.models.driver import DriverInstanceMdl
from py.srv.drivers.setpoints.models import SetpointParamsMdl


class SetpointDriver:
    __drivertype__ = 'setpoint'

    def add_endpoint(self, endpoint):
        logger.debug('Adding setpoint with name'.format(endpoint.name))
        self.data_from_ep(endpoint)

    def delete_endpoint(self, endpoint):
        logger.debug('Deleting setpoint with name {}'.format(endpoint.name))

    def update_endpoint(self, endpoint):
        logger.debug('Updating setpoint with uuid'.format(endpoint.uuid))
        self.data_from_ep(endpoint)

    @db_session
    def __init__(self, uuid, session):
        self.uuid = uuid

        endpoints = DriverInstanceMdl.get_instance_by_uuid(uuid=self.uuid, session=session).endpoints
        for endpoint in endpoints:
            self.data_from_ep(endpoint)

    @staticmethod
    def data_from_ep(endpoint):
        params = {endpoint.setpoint_params.name: pickle.loads(endpoint.setpoint_params.value)}
        DeviceSourceMdl.send_to_device(endpoint.uuid, params)
