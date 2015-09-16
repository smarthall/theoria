
class TheoriaException(Exception):
    pass

class ConfigException(TheoriaException):
    pass

class NotImplemented(TheoriaException):
    def __init__(self):
        super(NotImplemented, self).__init__('Called unimplemented code.')
