import pickle

from loguru import *

from py.srv import ServiceHub
from py.srv.database import db_session
from py.srv.database.models.device import DeviceSourceMdl
from py.srv.database.models.driver import DriverInstanceMdl
from py.srv.drivers.alarms.models import AlarmSeverityEnum
from py.srv.drivers.setpoints.models import SetpointParamsMdl
from py.srv.notifications import NotificationSrv


class AlarmDriver:
    __drivertype__ = 'alarm'

    def add_endpoint(self, endpoint):
        logger.debug('Adding alarm with name'.format(endpoint.name))
        self.data_from_ep(endpoint)

    def delete_endpoint(self, endpoint):
        logger.debug('Deleting alarm with name {}'.format(endpoint.name))

    def update_endpoint(self, endpoint):
        logger.debug('Updating alarm with uuid {}'.format(str(endpoint.uuid)))
        self.data_from_ep(endpoint)

    @db_session
    def __init__(self, uuid, session):
        self.uuid = uuid

        endpoints = DriverInstanceMdl.get_instance_by_uuid(uuid=self.uuid, session=session).endpoints
        for endpoint in endpoints:
            self.data_from_ep(endpoint)

    def data_to_ep(self, endpoint, params):
        if 'state' not in params.keys() or params['state'] is None:
            return
        ap = endpoint.alarm_params
        if ap.triggered == params['state']:
            return
        ap.set_state(state=params['state'])
        # TODO Should it be configured outside of the function?
        if bool(params['state']) is True:
            msg = ap.msg_on
            severity = ap.severity
        else:
            msg = ap.msg_off
            severity = AlarmSeverityEnum.Info
        ServiceHub.retrieve(NotificationSrv).new(msg,
                                                 severity.name,
                                                 ap.acl)

    @staticmethod
    def data_from_ep(endpoint):
        params = {'state': endpoint.alarm_params.triggered}
        DeviceSourceMdl.send_to_device(endpoint.uuid, params)
