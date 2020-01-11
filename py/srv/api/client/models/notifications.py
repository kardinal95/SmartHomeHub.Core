from py.srv.notifications import NotificationMdl


class NotificationDTO:
    def __init__(self, notification: NotificationMdl):
        self.uuid = notification.uuid
        self.msg = notification.msg
        self.severity = notification.severity
        self.timestamp = notification.timestamp

    def as_json(self):
        return {
            'uuid': str(self.uuid),
            'msg': self.msg,
            'severity': self.severity,
            'timestamp': self.timestamp.strftime('%d-%b-%Y (%H:%M:%S.%f)')
        }
