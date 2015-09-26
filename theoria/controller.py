"""
The Theoria main controller.
"""

import threading
import time

from importlib import import_module
from theoria.exceptions import ConfigException

def import_class(full_path):
    module_name, class_name = full_path.rsplit('.', 1)

    try:
        module = import_module(module_name)
    except ImportError:
        raise ConfigException('Error! Could not find module "%s"' % module_name)

    try:
        class_item = getattr(module, class_name)
    except AttributeError:
        raise ConfigException('Error! Could not find class "%s" in module "%s".' % (class_name, module_name))

    return getattr(module, class_name)

class Controller(threading.Thread):
    def __init__(self, config):
        # Create the Thread
        threading.Thread.__init__(self)
        self.name = 'Theoria-Controller'

        # Setup
        theoria_conf = config.get_global_section()

        ## Cache
        cache_conf = config.get_global_section('cache')
        cache_class = import_class(theoria_conf['cache'])
        self._cache = cache_class(**cache_conf)

        ## Provider
        providers = {}
        for provider_name in config.list_sections('provider'):
            providers[provider_name] = self.setup_provider(config.get_section('provider', provider_name))

        # Make constructors for screens
        screens = {}
        for screen_name in config.list_sections('screen'):
            screen_conf = config.get_section('screen', screen_name)

            def make_screen(buf, screens, screen_conf=screen_conf, providers=providers):
                conf = screen_conf.copy()
                screen_class = import_class(conf['screen'])
                del conf['screen']
                return screen_class(
                        buf=buf,
                        screens=screens,
                        providers=providers,
                        **conf
                )
            screens[screen_name] = make_screen

        # Check for a base screen
        if 'base' not in screens.keys():
            print 'No base screen found, cannot display anything.'
            return 1

        ## Driver
        driver_conf = config.get_global_section('driver')
        driver_class = import_class(theoria_conf['driver'])
        self._driver = driver_class(**driver_conf)

        # Instruct the screens to setup their linking if any
        base_screen = screens['base'](buf=self._driver.get_buffer(), screens=screens)
        base_screen.subscribe(self._driver.send_buffer)

        # Store the base screen
        self._base_screen = base_screen

    def setup_provider(self, provider_conf):
        provider_class = import_class(provider_conf['provider'])
        del provider_conf['provider']
        provider_conf['cache'] = self._cache
        return provider_class(**provider_conf)

    def run(self):
        self._running = True
        while self._running:
            time.sleep(0.1)

    def quit(self):
        self._running = False

