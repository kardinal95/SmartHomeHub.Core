import enum

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID

from py.srv import ServiceHub
from py.srv.database.models import DatabaseModel
from py.srv.redis import RedisSrv


class ConditionTypeEnum(enum.Enum):
    IsEqual = enum.auto(),
    IsMore = enum.auto(),
    IsLess = enum.auto(),
    NotEqual = enum.auto()


class ConditionMdl(DatabaseModel):
    __tablename__ = 'conditions'
    condition_type = Column(Enum(ConditionTypeEnum))
    scenario_uuid = Column(UUID(as_uuid=True), ForeignKey('scenarios.uuid'))
    source_dev_uuid = Column(UUID(as_uuid=True), ForeignKey('devices.uuid'))
    source_parameter = Column(String(64))
    target_dev_uuid = Column(UUID(as_uuid=True), ForeignKey('devices.uuid'))
    target_parameter = Column(String(64))

    def is_met(self):
        redis = ServiceHub.retrieve(RedisSrv)
        source = redis.hget(str(self.source_dev_uuid), self.source_parameter)
        target = redis.hget(str(self.target_dev_uuid), self.target_parameter)

        if self.condition_type == ConditionTypeEnum.IsEqual:
            return source == target
        if self.condition_type == ConditionTypeEnum.IsLess:
            return source < target
        if self.condition_type == ConditionTypeEnum.IsMore:
            return source > target
        if self.condition_type == ConditionTypeEnum.NotEqual:
            return source != target
