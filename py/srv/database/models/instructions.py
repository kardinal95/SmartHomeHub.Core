import enum
import pickle
import time

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import *

from py.srv import ServiceHub
from py.srv.database import db_session
from py.srv.database.models import DatabaseModel
from py.srv.database.models.device import DeviceMdl
from py.srv.redis import RedisSrv


class InstructionTypeEnum(enum.Enum):
    SetValue = enum.auto()
    WaitSec = enum.auto()


class InstructionMdl(DatabaseModel):
    __tablename__ = 'instructions'
    order = Column(Integer, nullable=False)
    scenario_uuid = Column(UUID(as_uuid=True), ForeignKey('scenarios.uuid'))
    instruction_type = Column(Enum(InstructionTypeEnum))
    parameters = relationship('InstructionParamsMdl',
                              backref=backref('instruction', uselist=False),
                              cascade='all, delete-orphan')

    @db_session
    def execute(self, session):
        params = dict([x.as_pair() for x in self.parameters])

        if self.instruction_type == InstructionTypeEnum.SetValue:
            source = DeviceMdl.get_device_with_uuid(uuid=str(params['source']),
                                                    session=session)
            target = DeviceMdl.get_device_with_uuid(uuid=str(params['target']),
                                                    session=session)
            kv = source.get_key_values()
            if params['s_param'] not in kv or params['t_param'] not in target.get_key_values():
                return
            ServiceHub.retrieve(RedisSrv).try_update(str(params['target']),
                                                     params['t_param'],
                                                      kv[params['s_param']])
            #ServiceHub.retrieve(RedisSrv).hset(str(params['target']),
            #                                   params['t_param'],
            #                                   kv[params['s_param']])
            target.decode()
        if self.instruction_type == InstructionTypeEnum.WaitSec:
            seconds = params['seconds']
            time.sleep(seconds)


class InstructionParamsMdl(DatabaseModel):
    __tablename__ = 'instruction_params'
    instruction_uuid = Column(UUID(as_uuid=True), ForeignKey('instructions.uuid'))
    name = Column(String(64))
    pickle_value = Column(Binary)

    def as_pair(self):
        return self.name, pickle.loads(self.pickle_value)