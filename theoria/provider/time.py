import pytz

from theoria.provider.base import PollingProvider
from datetime import datetime

DEFAULT_REFRESH_INTERVAL = 5

class Timezone(PollingProvider):
    def __init__(self, timezone, refresh_interval=DEFAULT_REFRESH_INTERVAL, *args, **kwargs):
        super(Timezone, self).__init__(refresh_interval, *args, **kwargs)

        self._timezone = pytz.timezone(timezone)

    def get_local_time(self):
        return self._timezone.localize(datetime.now())

    def provide(self):
        return {
                'time': self.get_local_time(),
                'timezone': self._timezone,
        }

