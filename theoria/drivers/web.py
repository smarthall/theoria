"""
A CherryPy driver for Theoria.
"""

import cherrypy
import threading
from PIL import Image
from cStringIO import StringIO
from base64 import b64encode
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket

def create(*args, **kwargs):
    return WebDriver(*args, **kwargs)

class WebDriver:
    def __init__(self, width=1024, height=600):
        self._width = int(width)
        self._height = int(height)

        self._web_thread = threading.Thread(target=self.start_web)
        self._web_thread.name = 'Theoria-WebDriver'
        self._web_thread.daemon = True
        self._web_thread.start()
        self._buffer = Image.new('RGB', (self._width, self._height))
        self.send_buffer()

    def get_buffer(self):
        return self._buffer

    def get_img_data(self):
        out = StringIO()
        self._buffer.save(out, 'PNG')
        imgdata = b64encode(out.getvalue())
        out.close()
        return imgdata

    def send_buffer(self):
        cherrypy.engine.publish('websocket-broadcast', self.get_img_data())

    def start_web(self):
        cherrypy.config.update({
            'server.socket_port': 9000,
            'engine.autoreload.on': False,
        })
        WebSocketPlugin(cherrypy.engine).subscribe()
        cherrypy.tools.websocket = WebSocketTool()
        cherrypy.quickstart(TheoriaWeb(self), '/', config={'/ws': {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': WebSocket
        }})

class TheoriaWeb(object):
    def __init__(self, driver):
        self._driver = driver

    @cherrypy.expose
    def index(self):
        return """
        <html>
        <head>
        <title>Theoria Web</title>
        <script type="text/javascript">
            var socket = new WebSocket('ws://localhost:9000/ws');
            socket.onmessage = function(e){
               var img = document.getElementById('image');
               img.src = "data:image/png;base64," + e.data;
            }
            socket.onclose = function (evt) {
               var img = document.getElementById('image');
               img.src = "";
            }
        </script>
        </head>
        <body>
        <h1>Theoria Web</h1>
        <img id="image" width="%d" height="%d" src="data:image/png;base64,%s" />
        </body>
        </html>
        """ % (self._driver._width, self._driver._height, self._driver.get_img_data())

    @cherrypy.expose
    def ws(self):
        pass

