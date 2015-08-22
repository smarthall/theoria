"""
Tools for running the app from the CLI
"""

import argparse
import sys
import signal
from importlib import import_module

import controller

def main():
    """
    Launch app from command line
    """
    parser = argparse.ArgumentParser(description='Start the metric monitor.')

    parser.add_argument("-d", "--driver", type=str,
            default="theoria.drivers.web",
            help="The driver for displaying the dash")

    parser.add_argument("-l", "--layout", type=str,
            default="theoria.layouts.fullscreen",
            help="The layout to use for displaying things")


    args = parser.parse_args()

    # Get the driver
    driver_module = import_module(args.driver)
    driver = driver_module.create()

    # Get the layout
    layout_module = import_module(args.layout)
    layout = layout_module.create()

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
            ctrlr._done = True

    print 'Theoria Exiting.'

    return 0

if __name__ == "__main__":
    sys.exit(main())

