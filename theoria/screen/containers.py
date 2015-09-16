from base import BaseScreen

class ContainerScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(ContainerString, self).__init__(self)

        self._str_children = kwargs['list']

    def link(self, buf, screens):
        super(ContainerString, self).link(buf, screens)

        # TODO: Grab our children from the args

class RotateScreen(ContainerScreen):
    def __init__(self, providers, list):
        pass

    def link(self, buf, screens):
        pass

    def draw(self):
        pass

