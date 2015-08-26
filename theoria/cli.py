"""
Tools for running the app from the CLI
"""

import argparse
from ConfigParser import SafeConfigParser
import sys
import signal
from importlib import import_module

import controller

def main():
    """
    Launch app from command line
    """
    parser = argparse.ArgumentParser(description='Start the metric monitor.')

    parser.add_argument("-c", "--config", type=str,
            default="conf/test.cfg",
            help="The configuration file to use")

    args = parser.parse_args()

    config = SafeConfigParser()
    config.read(['conf/default.cfg', args.config])
    theoria_conf = dict(config.items('theoria'))

    # Get the driver
    if 'theoria:driver' in config.sections():
        driver_conf = dict(config.items('theoria:driver'))
    else:
        driver_conf = {}
    driver_module = import_module(theoria_conf['driver'])
    driver = driver_module.create(**driver_conf)

    # Get the layout
    if 'theoria:layout' in config.sections():
        layout_conf = dict(config.items('theoria:layout'))
    else:
        layout_conf = {}
    layout_module = import_module(theoria_conf['layout'])
    layout = layout_module.create(driver=driver, **layout_conf)

    ctrlr = controller.Controller(
            driver=driver,
            layout=layout,
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

