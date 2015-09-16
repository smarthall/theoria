"""
Tools for running the app from the CLI
"""

import argparse
from ConfigParser import SafeConfigParser
import sys
import signal

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


def main():
    """
    Launch app from command line
    """
    parser = argparse.ArgumentParser(description='Start the metric monitor.')

    parser.add_argument("-c", "--config", type=str,
            default="conf/test.cfg",
            help="The configuration file to use")

    args = parser.parse_args()

    # Start up the controller
    config = TheoriaConfig()
    config.read(['conf/new.cfg', args.config])
    ctrlr = controller.Controller(config)
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

