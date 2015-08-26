"""
The Theoria main controller.
"""

import threading
import time
from Queue import Queue, Empty

from apps.color import ColorApp
from apps.clock import ClockApp

class Controller(threading.Thread):
    def __init__(self, driver, layout, cache, app_list):
        self._driver = driver
        self._layout = layout
        self._cache = cache
        self._app_list = app_list

        threading.Thread.__init__(self)
        self.name = 'Theoria-Controller'
        self._running = True

        for app in self._app_list:
            self._layout.register_app(app)

    def run(self):
        while self._running:
            time.sleep(0.5)

    def quit(self):
        self._running = False

