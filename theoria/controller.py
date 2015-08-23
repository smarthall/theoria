"""
The Theoria main controller.
"""

import threading
import time
from Queue import Queue, Empty

from apps.color import ColorApp
from apps.clock import ClockApp

class Controller(threading.Thread):
    def __init__(self, driver, layout_module):
        self._driver = driver

        imgbuffer = driver.get_buffer()
        trigger = self.process_update
        self._layout = layout_module.create(imgbuffer, trigger)

        self._applist = [
                ColorApp('#ff0000'),
                ClockApp(),
        ]

        threading.Thread.__init__(self)
        self.name = 'Theoria-Controller'
        self._running = True

        for app in self._applist:
            self._layout.register_app(app)

    def run(self):
        while self._running:
            time.sleep(0.5)

    def quit(self):
        self._running = False

    def process_update(self):
        self._driver.send_buffer()

