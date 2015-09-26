from theoria.exceptions import NotImplemented
from PIL import ImageColor, ImageDraw

DEFAULT_COLOR_SCREEN = '#000000'

class BaseScreen(object):
    def __init__(self, providers, buf, screens, provider=None):
        self._provider = providers.get(provider, None)

        self._subscribers = []

        self._buf = buf
        if self._provider is not None:
            self._provider.subscribe(
                    callback=self.draw
            )

    def subscribe(self, callback, *args, **kwargs):
        self._subscribers.append((callback, args, kwargs))

    def changed(self):
        for callback, args, kwargs in self._subscribers:
            callback(*args, **kwargs)

    def draw(self):
        raise NotImplemented()


class Color(BaseScreen):
    def __init__(self, color=DEFAULT_COLOR_SCREEN, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self._color = color

        self.draw()

    def draw(self):
        draw = ImageDraw.Draw(self._buf)

        x, y = self._buf.size

        draw.rectangle((0, 0, x, y), fill=self._color)
