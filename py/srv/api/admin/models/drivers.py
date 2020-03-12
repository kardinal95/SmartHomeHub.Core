from py.srv.database.models.driver import DriverInstanceMdl


class DriverDTO:
    def __init__(self, driver: DriverInstanceMdl):
        self.uuid = driver.uuid
        self.comment = driver.comment
        self.type = driver.driver_type
        self.parameters = driver.parameters

    def as_json(self):
        return {
            'uuid': self.uuid,
            'comment': self.comment,
            'type': self.type.name,
            'parameters': dict([x.get_as_pair() for x in self.parameters])
        }
