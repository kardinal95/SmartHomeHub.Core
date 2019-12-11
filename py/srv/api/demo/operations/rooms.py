from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from py.srv.api.exceptions import SimpleException
from py.srv.database import db_session
from py.srv.database.models.room import RoomMdl


@db_session
def get_all_rooms(session):
    return RoomMdl.get_all_rooms(session=session)


@db_session
def delete_rooms(rooms, session):
    for num, item in enumerate(rooms):
        try:
            delete_room(item=item, session=session)
        except UnmappedInstanceError as e:
            raise SimpleException('Item #{} not found. Stopping'.format(num))
    session.commit()


@db_session
def delete_room(item, session):
    room = RoomMdl.get_room_with_uuid(item)
    session.delete(room)
    session.flush()
    return room


@db_session
def add_rooms(rooms, session):
    for num, item in enumerate(rooms):
        try:
            add_room(item=item, session=session)
        except IntegrityError as e:
            raise SimpleException('Duplicate on #{} in sequence. Stopping'.format(num))
    session.commit()


@db_session
def add_room(item, session):
    room = RoomMdl(name=item)
    session.add(room)
    session.flush()
    return room
