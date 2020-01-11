import datetime

from sqlalchemy import Column, String, DateTime, func, Integer, desc

from py.srv.database import db_session
from py.srv.database.models import DatabaseModel
from py.srv.notifications.providers.socketio import SocketIOProvider


class NotificationMdl(DatabaseModel):
    __tablename__ = 'notifications'
    msg = Column(String(128))
    severity = Column(String(16))
    acl = Column(Integer)
    timestamp = Column(DateTime, server_default=func.now())

    @classmethod
    @db_session
    def create(cls, message, severity, acl, session):
        target = cls()
        target.msg = message
        target.severity = severity
        target.acl = acl
        session.add(target)
        session.commit()
        return target

    @classmethod
    @db_session
    def get_all(cls, session, limit=None):
        temp = session.query(cls).order_by(desc(cls.timestamp))
        if limit is None:
            return temp.all()
        return temp.limit(limit).all()


class NotificationSrv:
    providers = [SocketIOProvider(acl=999)]

    def __init__(self):
        pass

    @db_session
    def new(self, message, severity, acl, session):
        notification = NotificationMdl.create(message=message, severity=severity, acl=acl, session=session)
        for provider in self.providers:
            if provider.acl >= acl:
                provider.send(notification, acl)
