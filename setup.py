#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    # Project Details
    name='theoria',
    version='0.1',
    packages=['theoria'],

    # Dependencies
    install_requires=[
        'cherrypy',
        'pillow',
        'ws4py',
        'requests',
        'pytz',
        'funcsigs',
        'numpy',
        'setuptools>=17.1',
        'matplotlib',
        'pyusb==1.0.0b2',
    ],

    # Tests
    #test_suite="nose.collector",
    #tests_require = [
    #    'nose',
    #],

    entry_points = {
        'console_scripts': [
            'theoria = theoria.cli:main',
        ],
    },

    # Metadata for PyPI
    description='Lets you look at all your household data in a nice fashion.',
    author='Daniel Hall',
    author_email='theoria@danielhall.me',
    url='http://www.danielhall.me/',
)

