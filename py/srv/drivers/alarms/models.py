import enum

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from py.srv.database import db_session
from py.srv.database.models import DatabaseModel


class AlarmSeverityEnum(enum.Enum):
    Info = enum.auto()
    Warning = enum.auto()
    Error = enum.auto()
    Critical = enum.auto()


class AlarmParamsMdl(DatabaseModel):
    __tablename__ = 'alarm_params'
    ep_uuid = Column(UUID(as_uuid=True), ForeignKey('endpoints.uuid'))
    msg_on = Column(String(128))
    msg_off = Column(String(128))
    severity = Column(Enum(AlarmSeverityEnum))
    acl = Column(Integer)
    triggered = Column(Boolean, nullable=False)
    endpoint = relationship('EndpointMdl',
                            uselist=False,
                            backref=backref('alarm_params',
                                            uselist=False,
                                            cascade='all, delete-orphan'))

    @db_session
    def set_state(self, session, state):
        self.triggered = state
        session.add(session.merge(self))
        session.commit()