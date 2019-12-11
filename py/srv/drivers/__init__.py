from loguru import *

from py.srv.database.models.driver import *
from py.srv.drivers.mqtt.main import *

mapping = {
    DriverTypeEnum.mqtt: MqttDriver
}


class DriverSrv:
    instances = {}

    @db_session
    def __init__(self, session):
        items = session.query(DriverInstanceMdl).all()
        parameters = session.query(DriverParameterMdl).all()

        for item in items:
            self.add_instance(item, parameters)

    def get(self, uuid):
        return self.instances[uuid]

    def add_instance(self, instance, params):
        logger.info('Loading {type} driver with uuid {uuid}',
                    type=instance.driver_type,
                    uuid=instance.uuid)
        required = dict([x.get_as_pair() for x in params if x.driver_uuid == instance.uuid])
        driver = mapping[instance.driver_type](instance.uuid, **required)
        self.instances[instance.uuid] = driver