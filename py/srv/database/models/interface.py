from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from py.srv.database.models import DatabaseModel


class InterfaceMdl(DatabaseModel):
    __tablename__ = 'interfaces'
    device_uuid = Column(UUID(as_uuid=True), ForeignKey('devices.uuid'), unique=True)
    device = relationship('DeviceMdl', uselist=False)
    read_acl = Column(Integer)
    write_acl = Column(Integer)