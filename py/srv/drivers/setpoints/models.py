from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from py.srv.database.models import DatabaseModel


class SetpointParamsMdl(DatabaseModel):
    __tablename__ = 'setpoint_params'
    ep_uuid = Column(UUID(as_uuid=True), ForeignKey('endpoints.uuid'))
    name = Column(String(64))
    value = Column(Binary)
    endpoint = relationship('EndpointMdl',
                            uselist=False,
                            backref=backref('setpoint_params',
                                            uselist=True,
                                            cascade='all, delete-orphan'))