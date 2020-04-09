import pickle

from py.srv.database import db_session
from py.srv.database.models.endpoint import EndpointMdl
from py.srv.drivers.alarms.models import AlarmParamsMdl
from py.srv.drivers.mqtt.models import MqttParamsMdl, MqttTypeMdl
from py.srv.drivers.setpoints.models import SetpointParamsMdl


@db_session
def get_required_params(params, session):
    if params is MqttParamsMdl:
        return MqttParamsDTO(params=params, session=session)
    if params is SetpointParamsMdl:
        return SetpointParamsDTO(params=params)
    if params is AlarmParamsMdl:
        return AlarmParamsDTO(params=params)
    print('CRIT')


class EndpointDTO:
    def __init__(self, endpoint: EndpointMdl):
        self.uuid = endpoint.uuid
        self.name = endpoint.name
        self.driver_uuid = endpoint.driver_uuid
        self.driver_type = endpoint.driver_type
        self.driver_comment = endpoint.driver.comment

    def as_json(self):
        return {
            'uuid': str(self.uuid),
            'name': self.name,
            'driver': {
                'uuid': str(self.driver_uuid),
                'comment': self.driver_comment,
                'type': self.driver_type.name
            }
        }


class MqttParamsDTO:
    def __init__(self, params: MqttParamsMdl, session):
        self.topic_read = params.topic_read
        self.topic_write = params.topic_write
        self.type = MqttTypeMdl.get_by_uuid(uuid=params.type_uuid,
                                            session=session)

    def as_json(self):
        return {
            'topic_read': self.topic_read,
            'topic_write': self.topic_write,
            'type': self.type.name
        }


class SetpointParamsDTO:
    def __init__(self, params: SetpointParamsMdl):
        self.name = params.name
        self.value = pickle.loads(params.value)

    def as_json(self):
        return {
            'name': self.name,
            'value': self.value
        }


class AlarmParamsDTO:
    def __init__(self, params: AlarmParamsMdl):
        self.msg_on = params.msg_on
        self.msg_off = params.msg_off
        self.severity = params.severity
        self.acl = params.acl

    def as_json(self):
        return {
            'msg_on': self.msg_on,
            'msg_off': self.msg_off,
            'severity': self.severity.name,
            'acl': self.acl
        }
