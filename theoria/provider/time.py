from theoria.util import RepeatTimer
import pytz
from datetime import datetime

DEFAULT_REFRESH_INTERVAL = 5

class Timezone(object):
    def __init__(self, timezone, refresh_interval=DEFAULT_REFRESH_INTERVAL, *args, **kwargs):
        self._timezone = pytz.timezone(timezone)
        self._subscribers = []

        self._refresh_timer = RepeatTimer(
                interval=refresh_interval,
                callable=self.run,
        )
        self._refresh_timer.start()

    def get_local_time(self, time=None):
        if time is None:
            time = datetime.now()
        return self._timezone.localize(time)

    def subscribe(self, callback, *args, **kwargs):
        self._subscribers.append((callback, args, kwargs))
        callback(data=self.provide(), *args, **kwargs)

    def provide(self):
        return {
                'time': self.get_local_time(),
                'timezone': self._timezone,
        }

    def run(self):
        data = self.provide()
        for callback, args, kwargs in self._subscribers:
            callback(data=data, *args, **kwargs)

