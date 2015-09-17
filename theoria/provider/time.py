from theoria.util import RepeatTimer
import pytz
from datetime import datetime

class Timezone(object):
    def __init__(self, timezone, *args, **kwargs):
        self._timezone = pytz.timezone(timezone)
        self._subscribers = []

        self._refresh_timer = RepeatTimer(
                interval=1,
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

