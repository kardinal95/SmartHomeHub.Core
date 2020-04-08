from py.srv.database.models.endpoint import EndpointMdl


class EndpointDTO:
    def __init__(self, endpoint: EndpointMdl):
        self.uuid = endpoint.uuid
        self.name = endpoint.name
        self.driver_uuid = endpoint.driver_uuid
        self.driver_type = endpoint.driver_type
        self.driver_comment = endpoint.driver.comment

    def as_json(self):
        return {
            'uuid': str(self.uuid),
            'name': self.name,
            'driver': {
                'uuid': str(self.driver_uuid),
                'comment': self.driver_comment,
                'type': self.driver_type.name
            }
        }
