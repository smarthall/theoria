import datetime
import theoria.graphics as graphics
from PIL import ImageDraw, ImageColor, ImageFont
from theoria.util import RepeatTimer

DEFAULT_FONT='/usr/share/fonts/dejavu/DejaVuSans.ttf'
TIMEFMT_BIG = '%-I:%M:%S%p'
DATEFMT_BIG = '%A %d %B %Y'
TIMESIZE_BIG = 96
DATESIZE_BIG = 36

class ClockApp(object):
    def __init__(self, bgcolor='#000000', fgcolor='#ffffff', font=DEFAULT_FONT):
        self._bgcolor = ImageColor.getrgb(bgcolor)
        self._fgcolor = ImageColor.getrgb(fgcolor)
        self._timefontbig = ImageFont.truetype(font, size=TIMESIZE_BIG)
        self._datefontbig = ImageFont.truetype(font, size=DATESIZE_BIG)

        self._buffer = None
        self._trigger = None

        self._refresh = RepeatTimer(
                interval=1,
                callable=self._draw,
        )
        self._refresh.name = 'Theoria-ClockApp-Refresher'
        self._refresh.daemon = True
        self._refresh.start()

    def set_layout(self, imgbuf, trigger):
        self._buffer = imgbuf
        self._trigger = trigger

        self._draw()

    def _update_display(self):
        if self._trigger is not None:
            self._trigger()

    def _draw(self):
        if self._buffer is not None:
            draw = graphics.TheoriaDraw(self._buffer)

            bg1 = (0, 0)
            bg2 = (self._buffer.width, self._buffer.height)

            timestr = datetime.datetime.now().strftime(TIMEFMT_BIG)
            datestr = datetime.datetime.now().strftime(DATEFMT_BIG)

            textx = self._buffer.width / 2
            timey = self._buffer.height / 2
            datey = self._buffer.height / 2 + self._buffer.height / 8

            draw.rectangle((bg1, bg2), fill=self._bgcolor)
            draw.ctext((textx, timey), timestr, font=self._timefontbig, fill=self._fgcolor, center=graphics.CENTER_BOTH)
            draw.ctext((textx, datey), datestr, font=self._datefontbig, fill=self._fgcolor, center=graphics.CENTER_BOTH)
            self._trigger()

