from theoria.util import RepeatTimer
from theoria.exceptions import NotImplemented
import pytz
from datetime import datetime

class BaseProvider(object):
    def __init__(self, *args, **kwargs):
        self._subscribers = []

    def subscribe(self, callback, *args, **kwargs):
        self._subscribers.append((callback, args, kwargs))
        callback(data=self.provide(), *args, **kwargs)

    def run(self):
        data = self.provide()
        for callback, args, kwargs in self._subscribers:
            callback(data=data, *args, **kwargs)

    def provide(self):
        raise NotImplemented()

class PollingProvider(BaseProvider):
    def __init__(self, refresh_interval, *args, **kwargs):
        super(PollingProvider, self).__init__(*args, **kwargs)
        self._refresh_timer = RepeatTimer(
                interval=refresh_interval,
                callable=self.run,
        )
        self._refresh_timer.start()

