from sqlalchemy import *
from sqlalchemy.orm import *

from py.srv.database import db_session
from py.srv.database.models import DatabaseModel
from py.srv.database.models.condition import ConditionMdl # ORM
from py.srv.database.models.instructions import InstructionMdl # ORM


class ScenarioMdl(DatabaseModel):
    __tablename__ = 'scenarios'
    name = Column(String(64))
    description = Column(String(256))
    triggers = relationship('TriggerMdl', cascade='all, delete-orphan')
    conditions = relationship('ConditionMdl', cascade='all, delete-orphan')
    instructions = relationship('InstructionMdl', cascade='all, delete-orphan')

    @classmethod
    @db_session
    def get_by_uuid(cls, uuid, session):
        return session.query(cls).filter(cls.uuid == uuid).first()

    @classmethod
    @db_session
    def get_all(cls, session):
        return session.query(cls).all()
