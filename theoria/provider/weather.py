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

class Yahoo(object):
    ENDPOINT = 'https://query.yahooapis.com/v1/public/yql'
    FORECAST_YQL = 'select * from weather.forecast where woeid = {woeid}'

    def __init__(self, cache, woeid, *args, **kwargs):
        self._cache = cache
        self._woeid = woeid

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

    def provide(self):
        return {
                'weather': self.get_forecast(),
        }

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
        return (float(fahrenheit) - 32) / 1.8

    @property
    def title(self):
        return self._title

    @property
    def today(self):
        return self._data[0]

    @property
    def tomorrow(self):
        return self._data[1]

