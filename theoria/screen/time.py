from base import BaseScreen
from PIL import ImageColor, ImageFont
import theoria.graphics as graphics

DEFAULT_TIME_FORMAT = '%-I:%M%p'
DEFAULT_DATE_FORMAT = '%A %d %B %Y'
DEFAULT_FGCOLOR = '#ffffff'
DEFAULT_BGCOLOR = '#000000'
DEFAULT_FONT='/usr/share/fonts/dejavu/DejaVuSans.ttf'
DEFAULT_TIME_SIZE = 96
DEFAULT_DATE_SIZE = 36

class Time(BaseScreen):
    def __init__(self, time_format=DEFAULT_TIME_FORMAT, fgcolor=DEFAULT_FGCOLOR, bgcolor=DEFAULT_BGCOLOR, time_size=DEFAULT_TIME_SIZE, *args, **kwargs):
        super(Time, self).__init__(*args, **kwargs)

        self._time_format = time_format

        self._fgcolor = ImageColor.getrgb(fgcolor)
        self._bgcolor = ImageColor.getrgb(bgcolor)

        self._font = ImageFont.truetype(DEFAULT_FONT, time_size)

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

class TimeAndDate(BaseScreen):
    def __init__(self,
            time_format=DEFAULT_TIME_FORMAT,
            date_format=DEFAULT_DATE_FORMAT,
            fgcolor=DEFAULT_FGCOLOR,
            bgcolor=DEFAULT_BGCOLOR,
            time_size=DEFAULT_TIME_SIZE,
            date_size=DEFAULT_DATE_SIZE,
            *args, **kwargs):
        super(TimeAndDate, self).__init__(*args, **kwargs)

        self._time_format = time_format
        self._date_format = date_format

        self._fgcolor = ImageColor.getrgb(fgcolor)
        self._bgcolor = ImageColor.getrgb(bgcolor)

        self._timefont = ImageFont.truetype(DEFAULT_FONT, time_size)
        self._datefont = ImageFont.truetype(DEFAULT_FONT, date_size)

    def draw(self, data):
        draw = graphics.TheoriaDraw(self._buf)

        time_str = data['time'].strftime(self._time_format)
        date_str = data['time'].strftime(self._date_format)

        bg1 = (0, 0)
        bg2 = (self._buf.width, self._buf.height)

        textx = self._buf.width / 2
        timey = self._buf.height / 2
        datey =  self._buf.height / 2 + self._buf.height / 8

        draw.rectangle((bg1, bg2), fill=self._bgcolor)
        draw.ctext((textx, timey), time_str, font=self._timefont, fill=self._fgcolor, center=graphics.CENTER_BOTH)
        draw.ctext((textx, datey), date_str, font=self._datefont, fill=self._fgcolor, center=graphics.CENTER_BOTH)

        self.changed()

