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

def start_web():
    cherrypy.config.update({
        'server.socket_port': 9000,
        'engine.autoreload.on': False,
    })
    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()
    cherrypy.quickstart(TheoriaWeb(), '/', config={'/ws': {
        'tools.websocket.on': True,
        'tools.websocket.handler_cls': TheoriaWebSocket
    }})

class WebDriver:
    def __init__(self):
        self._web_thread = threading.Thread(target=start_web)
        self._web_thread.name = 'Theoria-WebDriver'
        self._web_thread.daemon = True
        self._web_thread.start()
        self._buffer = Image.new('RGB', (1024, 600))
        self.send_buffer()

    def get_buffer(self):
        return self._buffer

    def send_buffer(self):
        out = StringIO()
        self._buffer.save(out, 'PNG')
        imgdata = b64encode(out.getvalue())
        out.close()
        cherrypy.engine.publish('websocket-broadcast', imgdata)


class TheoriaWeb:
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
        </script>
        </head>
        <body>
        <h1>Theoria Web</h1>
        <img id="image" width="1024" height="600" />
        </body>
        </html>
        """

    @cherrypy.expose
    def ws(self):
        pass

class TheoriaWebSocket(WebSocket):
    pass

