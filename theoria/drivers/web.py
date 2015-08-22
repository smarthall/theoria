"""
A CherryPy driver for Theoria.
"""

import cherrypy
import threading
from PIL import Image

def create(*args, **kwargs):
    return WebDriver(*args, **kwargs)

def start_web():
    cherrypy.quickstart(TheoriaWeb())

class WebDriver:
    def __init__(self):
        self._web_thread = threading.Thread(target=start_web)
        self._web_thread.name = 'Theoria-Web'
        self._web_thread.daemon = True
        self._web_thread.start()
        self._buffer = Image.new('RGBA', (1024, 600))
        self.send_buffer()

    def get_buffer(self):
        return self._buffer

    def send_buffer(self):
        pass

class TheoriaWeb:
    @cherrypy.expose
    def index(self):
        return 'This is a test'

