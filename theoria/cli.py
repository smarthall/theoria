"""
Tools for running the app from the CLI
"""

import argparse
from ConfigParser import SafeConfigParser
import sys
import signal
from importlib import import_module

import controller

class TheoriaConfig(SafeConfigParser):
    def get_global_section(self):
        return dict(self.items('theoria'))

    def get_theoria_config_section(self, section):
        section = 'theoria:' + section

        if section in self.sections():
            return dict(self.items(section))
        else:
            return {}

    def get_app_list(self):
        sections = filter(lambda x:x.startswith('app:'), self.sections())
        return map(lambda x:x.split(':', 1)[1], sections)

    def get_app_config_section(self, app_name):
        app_name = 'app:' + app_name

        if app_name in self.sections():
            return dict(self.items(app_name))
        else:
            return {}


def import_class(full_path):
    module_name, class_name = full_path.rsplit('.', 1)

    module = import_module(module_name)

    return getattr(module, class_name)

def main():
    """
    Launch app from command line
    """
    parser = argparse.ArgumentParser(description='Start the metric monitor.')

    parser.add_argument("-c", "--config", type=str,
            default="conf/test.cfg",
            help="The configuration file to use")

    args = parser.parse_args()

    config = TheoriaConfig()
    config.read(['conf/default.cfg', args.config])
    theoria_conf = config.get_global_section()

    # Get the driver
    driver_conf = config.get_theoria_config_section('driver')
    driver_class = import_class(theoria_conf['driver'])
    driver = driver_class(**driver_conf)

    # Get the layout
    layout_conf = config.get_theoria_config_section('layout')
    layout_class = import_class(theoria_conf['layout'])
    layout = layout_class(driver=driver, **layout_conf)

    # Make a cache
    cache_conf = config.get_theoria_config_section('cache')
    cache_class = import_class(theoria_conf['cache'])
    cache = cache_class(**cache_conf)

    # Make all the apps
    app_list = []
    for app in config.get_app_list():
        app_conf = config.get_app_config_section(app)
        app_class = import_class(app_conf['app'])
        del app_conf['app']
        app_instance = app_class(**app_conf)
        app_list.append(app_instance)

    ctrlr = controller.Controller(
            driver=driver,
            layout=layout,
            cache=cache,
            app_list=app_list,
    )

    ctrlr.start()

    print 'Theoria started. Type CTRL-C to Exit.'

    done = False
    while not done:
        try:
            ctrlr.join(1)
        except KeyboardInterrupt:
            done = True
            ctrlr.quit()

    print 'Theoria Exiting.'

    return 0

if __name__ == "__main__":
    sys.exit(main())

