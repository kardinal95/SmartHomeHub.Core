from string import Template

import paho.mqtt.client as mqtt
from loguru import *

from py.srv import ServiceHub
from py.srv.database import db_session
from py.srv.database.models.device import DeviceSourceMdl
from py.srv.database.models.driver import DriverInstanceMdl
from py.srv.drivers.mqtt.models import MqttParamsMdl
from py.srv.redis import RedisSrv


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

        if len(targets) > 0:
            logger.debug('Subscribing on MQTT devices from database')
            self.client.subscribe(targets)

    def __init__(self, uuid, host, port, timeout=60, username=None, password=None):
        self.uuid = uuid
        # TODO Check if parameters exists
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect

        # TODO Connection errors
        logger.info('Connecting to mqtt server on {}:{}', host, port)
        if username is not None:
            self.client.username_pw_set(username, password)
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
        for item in parameters.items():
            ServiceHub.retrieve(RedisSrv).hset(params.endpoint.uuid, item[0], item[1])
        DeviceSourceMdl.send_to_device(params.endpoint.uuid, parameters)

    def data_to_ep(self, endpoint, params):
        topic = endpoint.mqtt_params.topic_write
        if topic is None or topic == '':
            return
        template = Template(endpoint.mqtt_params.type.write_template)
        self.client.publish(topic=topic, payload=template.substitute(**params))
