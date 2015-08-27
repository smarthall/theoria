from PIL import ImageDraw, ImageColor

class ColorApp(object):
    def __init__(self, color, *args, **kwargs):
        self._color = ImageColor.getrgb(color)

        self._buffer = None
        self._trigger = None

    def set_layout(self, imgbuf, trigger):
        self._buffer = imgbuf
        self._trigger = trigger

        self._draw()

    def _update_display(self):
        if self._trigger is not None:
            self._trigger()

    def _draw(self):
        if self._buffer is not None:
            draw = ImageDraw.Draw(self._buffer)

            x = self._buffer.width
            y = self._buffer.height

            draw.rectangle((0, 0, x, y), fill=self._color)
            self._trigger()

