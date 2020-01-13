from py.srv import ServiceHub
from py.srv.socketio import SocketIOSrv


class SocketIOProvider:
    def __init__(self, acl):
        self.acl = acl

    def send(self, notification, acl):
        ServiceHub.retrieve(SocketIOSrv).send_notification({
            'uuid': str(notification.uuid),
            'message': notification.msg,
            'severity': notification.severity,
            'time': notification.timestamp.timestamp()
        }, acl)
