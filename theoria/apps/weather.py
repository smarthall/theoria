import requests
from datetime import datetime
from PIL import ImageDraw, ImageColor, ImageFont
import theoria.graphics as graphics
from theoria.util import RepeatTimer

CACHE_TTL = 12*60
DEFAULT_UNITS = 'c'
DEFAULT_FONT='/usr/share/fonts/dejavu/DejaVuSans.ttf'
TITLE_FONTSIZE = 36
HEADER_FONTSIZE = 72
TEMP_FONTSIZE = 96

class ForecastApp(object):
    def __init__(self, cache, woeid, refresh=300, bgcolor="#000000", *args, **kwargs):
        self._cache = cache
        self._woeid = woeid
        self._refresh = refresh

        self._bgcolor = ImageColor.getrgb(bgcolor)
        self._fgcolor = ImageColor.getrgb('#ffffff')
        self._highcolor = ImageColor.getrgb('#ff0000')
        self._lowcolor = ImageColor.getrgb('#0000ff')

        self._titlefont = ImageFont.truetype(DEFAULT_FONT, size=TITLE_FONTSIZE)
        self._headerfont = ImageFont.truetype(DEFAULT_FONT, size=HEADER_FONTSIZE)
        self._tempfont = ImageFont.truetype(DEFAULT_FONT, size=TEMP_FONTSIZE)

        self._weather = YWeatherFetch(self._cache)

        self._buffer = None
        self._trigger = None

        self.get_forecast(False)

    def get_forecast(self, refresh):
        return self._weather.get_forecast(self._woeid)

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

            width = self._buffer.width
            height = self._buffer.height

            bg1 = (0, 0)
            bg2 = (width, height)

            centerw = width / 2

            draw.rectangle((bg1, bg2), fill=self._bgcolor)

            forecast = self.get_forecast(refresh=False)
            draw.ctext((centerw, 0), forecast.title, font=self._titlefont, fill=self._fgcolor, center=graphics.CENTER_HORIZ)

            loww = centerw - centerw / 2
            highw = centerw + centerw / 2

            # Today
            draw.ctext((centerw, 40), 'Today', font=self._headerfont, fill=self._fgcolor, center=graphics.CENTER_HORIZ)
            draw.ctext((loww, 140), str(int(forecast.today['low'])), font=self._tempfont, fill=self._lowcolor, center=graphics.CENTER_HORIZ)
            draw.ctext((centerw, 140), str(int(forecast.today['temp'])), font=self._tempfont, fill=self._fgcolor, center=graphics.CENTER_HORIZ)
            draw.ctext((highw, 140), str(int(forecast.today['high'])), font=self._tempfont, fill=self._highcolor, center=graphics.CENTER_HORIZ)

            # Tomorrow
            draw.ctext((centerw, 280), 'Tomorrow', font=self._headerfont, fill=self._fgcolor, center=graphics.CENTER_HORIZ)
            draw.ctext((loww, 360), str(int(forecast.tomorrow['low'])), font=self._tempfont, fill=self._lowcolor, center=graphics.CENTER_HORIZ)
            draw.ctext((highw, 360), str(int(forecast.tomorrow['high'])), font=self._tempfont, fill=self._highcolor, center=graphics.CENTER_HORIZ)

            self._update_display()

class YWeatherFetch(object):
    ENDPOINT = 'https://query.yahooapis.com/v1/public/yql'
    SEARCH_YQL = 'select woeid, name, country from geo.places where text="{search}"'
    FORECAST_YQL = 'select * from weather.forecast where woeid = {woeid}'

    def __init__(self, cache=None, units=DEFAULT_UNITS):
        self._cache = cache
        self._units = units

    def cache_key(self, data):
        return 'Theoria-YWeatherFetch-' + str(data)

    def _make_query(self, yql, refresh, **kwargs):
        data = {
            'q': yql.format(**kwargs),
            'format': 'json',
        }

        cached_value = None
        if self._cache is not None:
            cached_value = self._cache.get(self.cache_key(data))

        if refresh == False and cached_value is not None:
            return cached_value

        response = requests.get(YWeatherFetch.ENDPOINT, data)

        result = response.json()['query']['results']
        self._cache.store_item(self.cache_key(data), result, CACHE_TTL)

        return result

    def get_forecast(self, woeid, refresh=False):
        return WeatherData(self._make_query(YWeatherFetch.FORECAST_YQL, woeid=woeid, refresh=refresh))

    def find_woeid(self, search, refresh=False):
        return self._make_query(YWeatherFetch.SEARCH_YQL, search=search, refresh=refresh)

class WeatherData(object):
    DATE_FMT = '%d %b %Y'

    def __init__(self, json, units=DEFAULT_UNITS):
        self._units = units

        conditions = json['channel']['item']['condition']
        forecast = json['channel']['item']['forecast']
        todaystr = datetime.now().strftime(WeatherData.DATE_FMT)

        self._title = json['channel']['description']
        self._data = []

        if forecast[0]['date'] == todaystr:
            offset = 0
        else:
            offset = 1

        for i in range(0, 4):
            preprocessed = forecast[i + offset]
            data = {
                    'code': int(preprocessed['code']),
                    'high': self.from_fahrenheit(preprocessed['high']),
                    'low': self.from_fahrenheit(preprocessed['low']),
                    'date': datetime.strptime(preprocessed['date'], WeatherData.DATE_FMT),
                    'text': preprocessed['text'],
            }
            self._data.append(data)

        self._data[0]['temp'] = self.from_fahrenheit(conditions['temp'])

    def from_fahrenheit(self, fahrenheit):
        if self._units == 'c':
            return (float(fahrenheit) - 32) / 1.8
        else:
            return fahrenheit

    @property
    def title(self):
        return self._title

    @property
    def today(self):
        return self._data[0]

    @property
    def tomorrow(self):
        return self._data[1]

