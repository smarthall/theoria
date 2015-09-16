import time

from base import BaseScreen
from PIL import Image

DEFAULT_ROTATION_TIMER = 10


class ContainerScreen(BaseScreen):
    def __init__(self, *args, **kwargs):
        self._str_children = kwargs.pop('list').split(',')

        super(ContainerScreen, self).__init__(*args, **kwargs)

    def link(self, buf, screens):
        super(ContainerScreen, self).link(buf, screens)

        self._children = [screens[name] for name in self._str_children]


class RotateScreen(ContainerScreen):
    def __init__(self, refresh=DEFAULT_ROTATION_TIMER, *args, **kwargs):
        super(RotateScreen, self).__init__(*args, **kwargs)

        self._refresh = refresh

    def link(self, buf, screens):
        super(RotateScreen, self).link(buf, screens)

        bufsize = buf.size

        self._buffers = [Image.new('RGBA', bufsize) for scr in self._children]
        self._buffers = []
        for scr in self._children:
            scr_buf = Image.new('RGBA', bufsize)
            self._buffers.append(scr_buf)
            scr.link(scr_buf, screens)

    def draw(self):
        current = int(time.time() / self._refresh) % len(self._buffers)
        cbuf = self._buffers[current]

        self._buf.paste(cbuf, cbuf)

