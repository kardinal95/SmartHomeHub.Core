import paho.mqtt.client as mqtt
from loguru import *

from py.srv.database import db_session
from py.srv.database.models.device import DeviceSourceMdl
from py.srv.database.models.driver import DriverInstanceMdl
from py.srv.drivers.mqtt.models import MqttParamsMdl


class MqttDriver:
    __drivertype__ = 'mqtt'

    def add_endpoint(self, endpoint):
        logger.debug('Subscribing on MQTT device with name {}'.format(endpoint.name))
        self.client.subscribe(endpoint.mqtt_params.topic_read)

    def delete_endpoint(self, endpoint):
        logger.debug('Unsubscribing from MQTT device with name {}'.format(endpoint.name))
        self.client.unsubscribe(endpoint.mqtt_params.topic_read)

    @db_session
    def on_connect(self, client, userdata, flags, rc, session):
        logger.info('Connected with result code {}'.format(str(rc)))

        endpoints = DriverInstanceMdl.get_instance_by_uuid(uuid=self.uuid, session=session).endpoints
        targets = [(x.mqtt_params.topic_read, 0) for x in endpoints]

        logger.debug('Subscribing on MQTT devices from database')
        self.client.subscribe(targets)

    def __init__(self, uuid, host, port, timeout=60):
        self.uuid = uuid
        # TODO Check if parameters exists
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect

        # TODO Connection errors
        logger.info('Connecting to mqtt server on {}:{}', host, port)
        self.client.connect(host, port, timeout)

        self.client.loop_start()

    @staticmethod
    @db_session
    def on_message(client, userdata, msg, session):
        logger.debug('Received message on {} with data: {}'.format(msg.topic, msg.payload))

        params = MqttParamsMdl.get_params_by_topic_read(topic=msg.topic, session=session)
        MqttDriver.data_from_ep(payload=msg.payload, params=params)

    @staticmethod
    def data_from_ep(payload, params):
        parameters = params.type.as_dict(payload)
        DeviceSourceMdl.send_to_device(params.endpoint.uuid, parameters)
