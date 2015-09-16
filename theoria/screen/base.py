from theoria.exceptions import NotImplemented
from PIL import ImageColor, ImageDraw

class BaseScreen(object):
    def __init__(self, *args, **kwargs):
        all_providers = kwargs.pop('providers', [])
        str_provider = kwargs.pop('provider', None)

        self._provider = all_providers.get(str_provider, None)

        super(BaseScreen, self).__init__(*args, **kwargs)

    def link(self, buf, screens):
        self._buf = buf

    def draw(self):
        raise NotImplemented()


class Color(BaseScreen):
    def __init__(self, *args, **kwargs):
        self._color = ImageColor.getrgb(kwargs.pop('color', '#000000'))

    def link(self, buf, screens):
        super(Color, self).link(buf, screens)
        self.draw()

    def draw(self):
        draw = ImageDraw.Draw(self._buf)

        x, y = self._buf.size

        draw.rectangle((0, 0, x, y), fill=self._color)
