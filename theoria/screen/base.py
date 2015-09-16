from theoria.exceptions import NotImplemented

class BaseScreen(object):
    def __init__(self):
        super(BaseScreen, self).__init__(self)

    def link(self, buf, screens):
        self._buf = buf

    def draw(self):
        raise NotImplemented()

