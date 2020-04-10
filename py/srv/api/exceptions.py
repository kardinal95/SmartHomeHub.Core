from flask_jwt_extended.exceptions import *
from flask_restful import *
from jwt import *


def abort_on_exc(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IncorrectTargetException,
                JWTExtendedException,
                ExpiredSignatureError,
                SimpleException) as e:
            abort(404, message=str(e))
    return wrapper


class ApiOperationError(Exception):
    def __init__(self, msg, target):
        self.msg = msg
        self.target = target

    def __str__(self):
        return str({
            'msg': self.msg,
            'target': self.target
        })


class IncorrectTargetException(Exception):
    def __init__(self, uuid, target_type):
        self.uuid = uuid
        self.target_type = target_type

    def __str__(self):
        try:
            name = self.target_type.__short__
        except AttributeError:
            name = self.target_type.__name__
        return '{} with uuid {} does not exist'.format(name, self.uuid)


class SimpleException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg