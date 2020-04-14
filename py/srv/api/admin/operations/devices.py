import pickle
import uuid

from sqlalchemy.exc import IntegrityError

from py.srv import ServiceHub
from py.srv.api.exceptions import ApiOperationError
from py.srv.database import db_session
from py.srv.database.models.device import DeviceMdl
from py.srv.database.models.driver import DriverTypeEnum, DriverInstanceMdl
from py.srv.database.models.endpoint import EndpointMdl
from py.srv.drivers import DriverSrv
from py.srv.drivers.alarms.models import AlarmParamsMdl, AlarmSeverityEnum
from py.srv.drivers.mqtt.models import MqttParamsMdl, MqttTypeMdl
from py.srv.drivers.setpoints.models import SetpointParamsMdl


@db_session
def get_all_devices(session):
    return DeviceMdl.get_all_devices(session=session)