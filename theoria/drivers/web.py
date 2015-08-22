"""
A CherryPy driver for Theoria.
"""

import cherrypy
from PIL import Image

def create(*args, **kwargs):
    return WebDriver(*args, **kwargs)

class WebDriver:
    def __init__(self):
        self._buffer = Image.new('RGBA', (1024, 600))
        self.send_buffer()

    def get_buffer(self):
        return self._buffer

    def send_buffer(self):
        pass

