# vim: set fileencoding=utf-8 :
from base import BaseScreen
from PIL import ImageColor, ImageFont
import theoria.graphics as graphics

DEFAULT_FGCOLOR = '#ffffff'
DEFAULT_BGCOLOR = '#000000'
DEFAULT_HIGHCOLOR = '#ff0000'
DEFAULT_LOWCOLOR = '#0000ff'
DEFAULT_FONT='/usr/share/fonts/dejavu/DejaVuSans.ttf'
DEFAULT_TITLE_SIZE = 36
DEFAULT_HEADER_SIZE = 72
DEFAULT_TEMP_SIZE = 96

DEGREE_SIGN = u'°'

class Forecast(BaseScreen):
    def __init__(self,
            fgcolor=DEFAULT_FGCOLOR,
            bgcolor=DEFAULT_BGCOLOR,
            highcolor=DEFAULT_HIGHCOLOR,
            lowcolor=DEFAULT_LOWCOLOR,
            title_size=DEFAULT_TITLE_SIZE,
            header_size=DEFAULT_HEADER_SIZE,
            temp_size=DEFAULT_TEMP_SIZE,
            *args, **kwargs):
        super(Forecast, self).__init__(*args, **kwargs)

        self._bgcolor = ImageColor.getrgb(bgcolor)
        self._fgcolor = ImageColor.getrgb(fgcolor)
        self._highcolor = ImageColor.getrgb(highcolor)
        self._lowcolor = ImageColor.getrgb(lowcolor)

        self._titlefont = ImageFont.truetype(DEFAULT_FONT, size=title_size)
        self._headerfont = ImageFont.truetype(DEFAULT_FONT, size=header_size)
        self._tempfont = ImageFont.truetype(DEFAULT_FONT, size=temp_size)

        self.draw(self._provider.provide())

    def draw(self, data):
        draw = graphics.TheoriaDraw(self._buf)

        width, height = self._buf.size

        # Calculations
        centerw = width / 2
        loww = centerw - centerw / 2
        highw = centerw + centerw / 2

        # Fill background
        bg1 = (0, 0)
        bg2 = (width, height)
        draw.rectangle((bg1, bg2), fill=self._bgcolor)

        # Title
        draw.ctext((centerw, 0), data.title, font=self._titlefont, fill=self._fgcolor, center=graphics.CENTER_HORIZ)

        # Today
        draw.ctext((centerw, 40), 'Today', font=self._headerfont, fill=self._fgcolor, center=graphics.CENTER_HORIZ)
        draw.ctext((loww, 140), str(int(data.today['low'])), font=self._tempfont, fill=self._lowcolor, center=graphics.CENTER_HORIZ)
        draw.ctext((centerw, 140), str(int(data.today['temp'])), font=self._tempfont, fill=self._fgcolor, center=graphics.CENTER_HORIZ)
        draw.ctext((highw, 140), str(int(data.today['high'])), font=self._tempfont, fill=self._highcolor, center=graphics.CENTER_HORIZ)

        # Tomorrow
        draw.ctext((centerw, 280), 'Today', font=self._headerfont, fill=self._fgcolor, center=graphics.CENTER_HORIZ)
        draw.ctext((loww, 360), str(int(data.tomorrow['low'])), font=self._tempfont, fill=self._lowcolor, center=graphics.CENTER_HORIZ)
        draw.ctext((highw, 360), str(int(data.tomorrow['high'])), font=self._tempfont, fill=self._highcolor, center=graphics.CENTER_HORIZ)

        self.changed()

class TinyWeather(BaseScreen):
    def __init__(self,
            fgcolor=DEFAULT_FGCOLOR,
            bgcolor=DEFAULT_BGCOLOR,
            *args, **kwargs):
        super(TinyWeather, self).__init__(*args, **kwargs)

        self._bgcolor = ImageColor.getrgb(bgcolor)
        self._fgcolor = ImageColor.getrgb(fgcolor)

        width, height = self._buf.size
        self._tempfont = ImageFont.truetype(DEFAULT_FONT, size=width/2)
        self._titlefont = ImageFont.truetype(DEFAULT_FONT, size=24)

        self.draw(self._provider.provide())

    def draw(self, data):
        draw = graphics.TheoriaDraw(self._buf)

        width, height = self._buf.size

        # Calculations
        centerw = width / 2
        centerh = height / 2

        # Fill background
        bg1 = (0, 0)
        bg2 = (width, height)
        draw.rectangle((bg1, bg2), fill=self._bgcolor)

        # Text
        draw.ctext((centerw, 0), 'Currently', font=self._titlefont, fill=self._fgcolor, center=graphics.CENTER_HORIZ)
        draw.ctext((centerw, centerh), unicode(int(data.today['temp'])) + DEGREE_SIGN, font=self._tempfont, fill=self._fgcolor, center=graphics.CENTER_BOTH)

        self.changed()

class TinyForecast(BaseScreen):
    def __init__(self,
            fgcolor=DEFAULT_FGCOLOR,
            bgcolor=DEFAULT_BGCOLOR,
            highcolor=DEFAULT_HIGHCOLOR,
            lowcolor=DEFAULT_LOWCOLOR,
            day=0,
            *args, **kwargs):
        super(TinyForecast, self).__init__(*args, **kwargs)

        self._bgcolor = ImageColor.getrgb(bgcolor)
        self._fgcolor = ImageColor.getrgb(fgcolor)
        self._highcolor = ImageColor.getrgb(highcolor)
        self._lowcolor = ImageColor.getrgb(lowcolor)

        width, height = self._buf.size
        self._tempfont = ImageFont.truetype(DEFAULT_FONT, size=int(width / 2.5))
        self._titlefont = ImageFont.truetype(DEFAULT_FONT, size=24)

        self._day = int(day)

        self.draw(self._provider.provide())

    def draw(self, data):
        draw = graphics.TheoriaDraw(self._buf)

        width, height = self._buf.size

        # Calculations
        centerw = width / 2
        third = height / 3
        highh = third - (third / 2)
        lowh = third * 2 - (third / 2)

        # Strings
        forecast = data.day(self._day)
        high = unicode(int(forecast['high'])) + DEGREE_SIGN
        low  = unicode(int(forecast['low'])) + DEGREE_SIGN

        if self._day == 0:
            title = 'Today'
        elif self._day == 1:
            title = 'Tomorrow'
        else:
            title = forecast['date'].strftime('%A')

        # Fill background
        bg1 = (0, 0)
        bg2 = (width, height)
        draw.rectangle((bg1, bg2), fill=self._bgcolor)

        # Title
        draw.ctext((centerw, 0), title, font=self._titlefont, fill=self._fgcolor, center=graphics.CENTER_HORIZ)

        # Today
        draw.ctext((centerw, highh), high, font=self._tempfont, fill=self._highcolor, center=graphics.CENTER_HORIZ)
        draw.ctext((centerw, lowh), low, font=self._tempfont, fill=self._lowcolor, center=graphics.CENTER_HORIZ)

        self.changed()

