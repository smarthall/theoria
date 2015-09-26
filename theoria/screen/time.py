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

        self.draw(self._provider.provide())

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

class TinyTime(BaseScreen):
    def __init__(self, fgcolor=DEFAULT_FGCOLOR, bgcolor=DEFAULT_BGCOLOR, *args, **kwargs):
        super(TinyTime, self).__init__(*args, **kwargs)

        self._fgcolor = ImageColor.getrgb(fgcolor)
        self._bgcolor = ImageColor.getrgb(bgcolor)

        width, height = self._buf.size
        self._font = ImageFont.truetype(DEFAULT_FONT, int(height / 2.5))

        self.draw(self._provider.provide())

    def draw(self, data):
        draw = graphics.TheoriaDraw(self._buf)

        hours   = data['time'].strftime('%-I')
        minutes = data['time'].strftime('%-M')

        bg1 = (0, 0)
        bg2 = (self._buf.width, self._buf.height)

        textx = self._buf.width / 2

        draw.rectangle((bg1, bg2), fill=self._bgcolor)
        draw.ctext((textx, 0), hours, font=self._font, fill=self._fgcolor, center=graphics.CENTER_HORIZ)
        draw.ctext((textx, self._buf.height/2), minutes, font=self._font, fill=self._fgcolor, center=graphics.CENTER_HORIZ)

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

        self.draw(self._provider.provide())

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

class TinyYear(BaseScreen):
    def __init__(self, fgcolor=DEFAULT_FGCOLOR, bgcolor=DEFAULT_BGCOLOR, *args, **kwargs):
        super(TinyYear, self).__init__(*args, **kwargs)

        self._fgcolor = ImageColor.getrgb(fgcolor)
        self._bgcolor = ImageColor.getrgb(bgcolor)

        width, height = self._buf.size
        self._font = ImageFont.truetype(DEFAULT_FONT, width / 3)

        self.draw(self._provider.provide())

    def draw(self, data):
        draw = graphics.TheoriaDraw(self._buf)

        year = data['time'].strftime('%Y')

        bg1 = (0, 0)
        bg2 = (self._buf.width, self._buf.height)

        textx = self._buf.width / 2
        texty = self._buf.height / 2

        draw.rectangle((bg1, bg2), fill=self._bgcolor)
        draw.ctext((textx, texty), year, font=self._font, fill=self._fgcolor, center=graphics.CENTER_BOTH)

        self.changed()

class TinyDate(BaseScreen):
    def __init__(self, fgcolor=DEFAULT_FGCOLOR, bgcolor=DEFAULT_BGCOLOR, *args, **kwargs):
        super(TinyDate, self).__init__(*args, **kwargs)

        self._fgcolor = ImageColor.getrgb(fgcolor)
        self._bgcolor = ImageColor.getrgb(bgcolor)

        width, height = self._buf.size
        self._numfont = ImageFont.truetype(DEFAULT_FONT, height / 2)
        self._wordfont = ImageFont.truetype(DEFAULT_FONT, height / 8)

        self.draw(self._provider.provide())

    def draw(self, data):
        draw = graphics.TheoriaDraw(self._buf)

        # Text
        dayname = data['time'].strftime('%A')
        day = data['time'].strftime('%-d')
        monthname = data['time'].strftime('%B')

        # Calculations
        bg1 = (0, 0)
        bg2 = (self._buf.width, self._buf.height)

        textx = self._buf.width / 2
        daynamey = self._buf.height / 8
        dayy = self._buf.height / 2
        monthnamey = self._buf.height - (self._buf.height / 4)

        # Drawing
        draw.rectangle((bg1, bg2), fill=self._bgcolor)
        draw.ctext((textx, daynamey), dayname, font=self._wordfont, fill=self._fgcolor, center=graphics.CENTER_HORIZ)
        draw.ctext((textx, dayy), day, font=self._numfont, fill=self._fgcolor, center=graphics.CENTER_BOTH)
        draw.ctext((textx, monthnamey), monthname, font=self._wordfont, fill=self._fgcolor, center=graphics.CENTER_HORIZ)

        self.changed()

