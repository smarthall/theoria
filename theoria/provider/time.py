from theoria.util import RepeatTimer
import pytz
from datetime import datetime

class Timezone(object):
    def __init__(self, timezone, *args, **kwargs):
        self._timezone = pytz.timezone(timezone)

    def get_local_time(self, time=datetime.now()):
        return self._timezone.localize(time)

    def provide(self):
        return {
                'time': self.get_local_time(),
                'timezone': self._timezone,
        }

