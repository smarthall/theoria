from theoria.util import RepeatTimer

def create(*args, **kwargs):
    return FullscreenLayout(*args, **kwargs)

class FullscreenLayout:
    def __init__(self, imgbuffer, trigger):
        self._trigger = trigger
        self._buffer = imgbuffer

        self._applist = []
        self._cur_app = 0

        self._rotate_timer = RepeatTimer(
                interval=10,
                callable=self._rotate_screen,
        )
        self._rotate_timer.daemon = True
        self._rotate_timer.name = 'Theoria-FullscreenLayout-Rotater'
        self._rotate_timer.start()

    def register_app(self, app):
        self._applist.append(app)
        if len(self._applist) == 1:
            app.set_layout(self._buffer, self._trigger)

    def deregister_app(self, app):
        self._applist.remove(app)

    def _get_cur_app(self):
        if len(self._applist) > 0:
            return self._applist[self._cur_app]
        else:
            return None #TODO: Return blank screen

    def _get_next_app(self):
        if len(self._applist) > 0:
            self._cur_app = (self._cur_app + 1) % len(self._applist)

        return self._get_cur_app()

    def _rotate_screen(self):
        oldapp = self._get_cur_app()
        newapp = self._get_next_app()

        if oldapp is not None:
            oldapp.set_layout(None, None)
        if newapp is not None:
            newapp.set_layout(self._buffer, self._trigger)
