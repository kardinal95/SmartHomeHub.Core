from py.srv.database.models.room import RoomMdl


class RoomDTO:
    def __init__(self, room: RoomMdl):
        self.uuid = room.uuid
        self.name = room.name

    def as_json(self):
        return {
            'uuid': str(self.uuid),
            'name': self.name
        }
