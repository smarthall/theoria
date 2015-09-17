from base import BaseScreen
from PIL import Image
from theoria.util import RepeatTimer

DEFAULT_ROTATION_TIMER = 10


class ContainerScreen(BaseScreen):
    def __init__(self, *args, **kwargs):
        self._str_children = kwargs.pop('list').split(',')

        super(ContainerScreen, self).__init__(*args, **kwargs)

    def link(self, buf, screens):
        super(ContainerScreen, self).link(buf, screens)

        self._children = []
        for name in self._str_children:
            screen = screens[name]
            num = len(self._children)
            self._children.append(screen)
            screen.subscribe(
                    callback=self.child_changed,
            )

    def child_changed(self):
        self.draw()
        self.changed()

class RotateScreen(ContainerScreen):
    def __init__(self, refresh=DEFAULT_ROTATION_TIMER, *args, **kwargs):
        super(RotateScreen, self).__init__(*args, **kwargs)

        self._current = 0

        self._next_timer = RepeatTimer(
                interval = refresh,
                callable=self.next,
        )

    def link(self, buf, screens):
        super(RotateScreen, self).link(buf, screens)

        bufsize = buf.size

        self._buffers = [Image.new('RGBA', bufsize) for scr in self._children]
        self._buffers = []
        for scr in self._children:
            scr_buf = Image.new('RGBA', bufsize)
            self._buffers.append(scr_buf)
            scr.link(scr_buf, screens)

        self._next_timer.start()
        self.draw()

    def next(self):
        self._current = (self._current + 1) % len(self._buffers)
        self.draw()
        self.changed()

    def draw(self):
        cbuf = self._buffers[self._current]

        self._buf.paste(cbuf, (0, 0), cbuf)

