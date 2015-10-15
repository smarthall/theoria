from base import BaseScreen
from PIL import Image
from theoria.util import RepeatTimer
from theoria.exceptions import ConfigException
from datetime import datetime

DEFAULT_ROTATION_TIMER = 10


class ContainerScreen(BaseScreen):
    def __init__(self, screens, children, *args, **kwargs):
        super(ContainerScreen, self).__init__(screens=screens, *args, **kwargs)

        self._children = []
        i = 0;
        for name in children.split(','):
            newbuf = self.make_buffer(i, name)
            screen = screens[name](screens=screens, buf=newbuf)
            self._children.append(screen)
            screen.subscribe(
                    callback=self.child_changed,
            )
            i += 1

    def make_buffer(self, num, name):
        raise NotImplemented('Children of ContainerScreen need to override this.')

    def child_changed(self):
        self.draw()
        self.changed()

class ConditionalScreen(BaseScreen):
    def __init__(self, buf, screens, true, false, condition, *args, **kwargs):
        self._bufsize = buf.size

        super(ConditionalScreen, self).__init__(buf=buf, screens=screens, *args, **kwargs)

        # Make buffers
        self._truebuf = Image.new('RGBA', self._bufsize)
        self._falsebuf = Image.new('RGBA', self._bufsize)

        # Make screens
        truescreen = screens[true](screens=screens, buf=self._truebuf)
        falsescreen = screens[false](screens=screens, buf=self._falsebuf)

        # Subscribe to their changes
        truescreen.subscribe(callback=self.child_changed)
        falsescreen.subscribe(callback=self.child_changed)

        # Compile the condition
        self._condition = compile(condition, '<string>', 'eval')

    def condition(self):
        return eval(self._condition, {}, {
            'now': datetime.now(),
        })

    def child_changed(self):
        self.draw()
        self.changed()

    def draw(self):
        result = self.condition()

        if result:
            cbuf = self._truebuf
        else:
            cbuf = self._falsebuf

        self._buf.paste(cbuf, (0, 0), cbuf)

class RotateScreen(ContainerScreen):
    def __init__(self, buf, refresh=DEFAULT_ROTATION_TIMER, *args, **kwargs):
        self._bufsize = buf.size
        self._buffers = []

        super(RotateScreen, self).__init__(buf=buf, *args, **kwargs)

        self._current = 0
        self._next_timer = RepeatTimer(
                interval = refresh,
                callable=self.next,
        )
        self._next_timer.start()

        self.draw()

    def make_buffer(self, num, name):
        newbuf = Image.new('RGBA', self._bufsize)
        self._buffers.append(newbuf)
        return newbuf

    def next(self):
        self._current = (self._current + 1) % len(self._buffers)
        self.draw()
        self.changed()

    def draw(self):
        cbuf = self._buffers[self._current]

        self._buf.paste(cbuf, (0, 0), cbuf)

class GridScreen(ContainerScreen):
    def __init__(self, buf, rows=2, cols=2, *args, **kwargs):
        width, height = buf.size
        self._bufsize = (width / int(cols), height / int(rows))
        self._buffers = {}
        self._cols = int(cols)
        self._rows = int(rows)

        super(GridScreen, self).__init__(buf=buf, *args, **kwargs)

        if len(self._children) != (self._rows * self._cols):
            raise ConfigException('Expected %s screens, but got %s.' % ((self._rows * self._cols), len(self._children)))

        self.draw()

    def make_buffer(self, num, name):
        pos = (num / self._cols, num % self._cols)
        newbuf = Image.new('RGBA', self._bufsize)
        self._buffers[pos] = newbuf
        return newbuf

    def draw(self):
        for pos, buf in self._buffers.iteritems():
            r, c = pos
            bufw, bufh = self._bufsize
            drawx = c * bufw
            drawy = r * bufh

            self._buf.paste(buf, (drawx, drawy), buf)

        self.changed()

class ConditionalTimeScreen(ContainerScreen):
    def __init__(self, buf, *args, **kwargs):
        width, height = buf.size
        self._bufsize = (width / int(cols), height / int(rows))
        self._buffers = {}
        self._cols = int(cols)
        self._rows = int(rows)

        super(GridScreen, self).__init__(buf=buf, *args, **kwargs)

        if len(self._children) != (self._rows * self._cols):
            raise ConfigException('Expected %s screens, but got %s.' % ((self._rows * self._cols), len(self._children)))

        self.draw()

    def make_buffer(self, num, name):
        pos = (num / self._cols, num % self._cols)
        newbuf = Image.new('RGBA', self._bufsize)
        self._buffers[pos] = newbuf
        return newbuf

    def draw(self):
        for pos, buf in self._buffers.iteritems():
            r, c = pos
            bufw, bufh = self._bufsize
            drawx = c * bufw
            drawy = r * bufh

            self._buf.paste(buf, (drawx, drawy), buf)

        self.changed()


