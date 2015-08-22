"""
The Theoria main controller.
"""

import threading
from Queue import Queue, Empty

from util import RepeatTimer

class Controller(threading.Thread):
    def __init__(self, driver):
        threading.Thread.__init__(self)
        self.name = 'Theoria-Controller'
        self._driver = driver
        self._update_queue = Queue()
        self._done = False
        self._timer = RepeatTimer(5, self._driver.send_buffer)
        self._timer.daemon = True

    def run(self):
        self._timer.start()
        while not self._done:
            try:
                (args, kwargs) = self._update_queue.get(True, 1)
                self._process_update(*args, **kwargs)
            except Empty:
                pass

    def quit(self):
        self._done = True

    def queue_update(self, *args, **kwargs):
        self._update_queue.put((args, kwargs))

    def process_update(self):
        self._driver.get_buffer()
        # Perform update
        self._driver.send_buffer()

