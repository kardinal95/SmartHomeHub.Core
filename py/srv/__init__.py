from loguru import logger


class ServiceHub:
    services = dict()

    @staticmethod
    def register(srv: object, srv_class: type) -> None:
        if srv_class in ServiceHub.services.keys():
            raise Exception('Already exists!')
        ServiceHub.services[srv_class] = srv
        logger.info('Service {} registered'.format(srv_class.__name__))

    @staticmethod
    def forget(srv_class: type) -> None:
        if srv_class not in ServiceHub.services.keys():
            raise Exception('No registered service of such class found!')
        del(ServiceHub.services[srv_class])
        logger.info('Service {} removed'.format(srv_class.__name__))

    @staticmethod
    def retrieve(srv_class: type):
        if srv_class in ServiceHub.services.keys():
            return ServiceHub.services[srv_class]
        return None
