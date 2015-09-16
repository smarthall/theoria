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

        # Screen
        screens = {}
        for screen_name in config.list_sections('screen'):
            screens[screen_name] = self.setup_screen(config.get_section('screen', screen_name), providers)

        # Check for a base screen
        if 'base' not in screens.keys():
            print 'No base screen found, cannot display anything.'
            return 1

        ## Driver
        driver_conf = config.get_global_section('driver')
        driver_class = import_class(theoria_conf['driver'])
        self._driver = driver_class(**driver_conf)

        # Instruct the screens to setup their linking if any
        base_screen = screens['base']
        base_screen.link(self._driver.get_buffer(), screens)

        # Store the base screen
        self._base_screen = base_screen

    def setup_provider(self, provider_conf):
        provider_class = import_class(provider_conf['provider'])
        del provider_conf['provider']
        provider_conf['cache'] = self._cache
        return provider_class(**provider_conf)

    def setup_screen(self, screen_conf, providers):
        screen_class = import_class(screen_conf['screen'])
        del screen_conf['screen']
        return screen_class(providers=providers, **screen_conf)

    def run(self):
        self._running = True
        while self._running:
            self._base_screen.draw()
            self._driver.send_buffer()
            time.sleep(0.1)

    def quit(self):
        self._running = False

