from py.srv.database.models.endpoint import EndpointMdl


class DemoEndpointDTO:
    def __init__(self, endpoint: EndpointMdl):
        self.uuid = endpoint.uuid
        self.type = endpoint.driver_type
        self.name = endpoint.name

    def as_json(self):
        return {
            'uuid': str(self.uuid),
            'name': self.name,
            'type': self.type.name
        }