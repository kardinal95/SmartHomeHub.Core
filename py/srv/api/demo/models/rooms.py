class DemoRoomDTO:
    def __init__(self, room):
        self.uuid = room.uuid
        self.name = room.name

    def as_json(self):
        return {
            'uuid': str(self.uuid),
            'name': self.name
        }
