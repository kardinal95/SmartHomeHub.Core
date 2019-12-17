from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from py.srv.database import db_session
from py.srv.database.models import DatabaseModel
from py.srv.database.models.scenario import ScenarioMdl # ORM


class TriggerMdl(DatabaseModel):
    __tablename__ = 'triggers'
    comment = Column(String(128))
    scenario_uuid = Column(UUID(as_uuid=True), ForeignKey('scenarios.uuid'))
    scenario = relationship('ScenarioMdl', uselist=False)
    device_uuid = Column(UUID(as_uuid=True), ForeignKey('devices.uuid'))
    parameter = Column(String(64))

    @classmethod
    @db_session
    def get_by_parameters(cls, uuid, parameters, session):
        return session.query(cls)\
            .filter(cls.device_uuid == uuid)\
            .filter(cls.parameter.in_(parameters))\
            .all()
