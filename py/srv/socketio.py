import string
import random

import socketio
from loguru import logger

from py.srv import ServiceHub
from py.srv.database import db_session
from py.srv.database.models.device import DeviceMdl


def id_generator(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


class SocketIOSrv:
    access = None
    room_map = None
    sio = socketio.Server(cors_allowed_origins='*', ping_timeout=30000, ping_interval=30000)

    def __init__(self, flask, redis):
        self.rooms = dict()
        self.room_map = dict()
        self.access = dict()
        self.app = socketio.WSGIApp(self.sio, flask.app)
        #self.sio.attach(flask.app, socketio_path='socketio')
        redis.subscribe(self.on_update)

    def generate_key(self, uuid, acl):
        self.access[str(uuid)] = (id_generator(size=32), acl)
        return self.access[str(uuid)][0]

    @db_session
    def on_update(self, uuid, key_values, session):
        dev = DeviceMdl.get_device_with_uuid(uuid=uuid, session=session)
        if dev is None:
            return
        parameters = {x[0]: x[1] for x in key_values.items() if x[0] in dev.get_key_values()}
        if len(parameters) == 0:
            return
        if dev.interface is None:
            return
        acl = dev.interface.read_acl
        for key in self.room_map.keys():
            logger.info('Checking for acl {}. Acl of device is {}'.format(str(key), str(acl)))
            if key >= acl:
                for item in self.room_map[key]:
                    logger.info('Sending state of {} to {}'.format(str(uuid), str(item)))
                    self.sio.emit('state', {'uuid': uuid,
                                            'parameters': key_values}, room=item)

    def add_to_room(self, acl, sid):
        if acl not in self.room_map.keys():
            self.room_map[acl] = list()
        self.room_map[acl].append(sid)

    def delete_from_room(self, sid):
        for key in self.room_map.keys():
            if sid in self.room_map[key]:
                self.room_map[key].remove(sid)
                if len(self.room_map[key]) == 0:
                    del(self.room_map[key])
                    return


@SocketIOSrv.sio.event
def authenticate(sid, data):
    io = ServiceHub.retrieve(SocketIOSrv)
    if 'key' not in data.keys():
        io.sio.emit('incorrect', {'message': 'incorrect authentication'})
    for uuid in io.access.keys():
        if io.access[uuid][0] == data['key']:
            io.add_to_room(io.access[uuid][1], sid)
            io.sio.emit('correct', {'message': 'successful authentication'})


@SocketIOSrv.sio.event
def connect(sid, environ=None):
    logger.debug('Connection from sid {}'.format(sid))


@SocketIOSrv.sio.event
def disconnect(sid):
    logger.debug('Disconnecting socketio user with sid {}'.format(sid))
    ServiceHub.retrieve(SocketIOSrv).delete_from_room(sid)
