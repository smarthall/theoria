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
    def get_global_section(self, name=None):
        if name is None:
            return dict(self.items('theoria'))
        else:
            return self.get_section('theoria', name)

    def get_section(self, section_type, name):
        section = section_type + ':' + name

        if section in self.sections():
            return dict(self.items(section))
        else:
            return {}

    def list_sections(self, section_type):
        section_prefix = section_type + ':'

        sections = filter(lambda x:x.startswith(section_prefix), self.sections())
        return map(lambda x:x.split(':', 1)[1], sections)


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
    config.read(['conf/new.cfg', args.config])
    theoria_conf = config.get_global_section()

    # Get the driver
    driver_conf = config.get_global_section('driver')
    driver_class = import_class(theoria_conf['driver'])
    driver = driver_class(**driver_conf)

    # Make a cache
    cache_conf = config.get_global_section('cache')
    cache_class = import_class(theoria_conf['cache'])
    cache = cache_class(**cache_conf)

    # Start up all the providers
    providers = {}
    for provider_name in config.list_sections('provider'):
        # Find the provider
        provider_conf = config.get_section('provider', provider_name)

        try:
            provider_class = import_class(provider_conf['provider'])
        except ImportError as e:
            print 'Error! Could not find provider: ' + provider_conf['provider']
            sys.exit(1)

        # Prepare the provider config
        del provider_conf['provider']
        provider_conf['cache'] = cache
        provider_instance = provider_class(**provider_conf)

        # Store it for later
        providers[provider_name] = provider_instance

    # Build the screen starting from the base
    base_screen = None

    ctrlr = controller.Controller(
            driver=driver,
            base_screen=base_screen,
            cache=cache,
            providers=providers,
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

