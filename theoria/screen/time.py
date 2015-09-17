from base import BaseScreen
from PIL import ImageColor, ImageFont
import theoria.graphics as graphics

DEFAULT_TIME_FORMAT = '%-I:%M:%S%p'
DEFAULT_FGCOLOR = '#ff0000'
DEFAULT_BGCOLOR = '#000000'
DEFAULT_FONT='/usr/share/fonts/dejavu/DejaVuSans.ttf'

class Time(BaseScreen):
    def __init__(self, time_format=DEFAULT_TIME_FORMAT, fgcolor=DEFAULT_FGCOLOR, bgcolor=DEFAULT_BGCOLOR, *args, **kwargs):
        super(Time, self).__init__(*args, **kwargs)

        self._time_format = time_format

        self._fgcolor = ImageColor.getrgb(fgcolor)
        self._bgcolor = ImageColor.getrgb(bgcolor)

        self._font = ImageFont.truetype(DEFAULT_FONT, 96)

    def draw(self, data):
        draw = graphics.TheoriaDraw(self._buf)

        time_str = data['time'].strftime(self._time_format)

        bg1 = (0, 0)
        bg2 = (self._buf.width, self._buf.height)

        textx = self._buf.width / 2
        timey = self._buf.height / 2

        draw.rectangle((bg1, bg2), fill=self._bgcolor)
        draw.ctext((textx, timey), time_str, font=self._font, fill=self._fgcolor, center=graphics.CENTER_BOTH)

        self.changed()

