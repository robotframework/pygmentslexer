#!/usr/bin/env python

"""Pygments lexer for Robot Framework test data."""

from os.path import abspath, dirname, join
import re

from setuptools import setup

NAME = 'robotframeworklexer'
CLASSIFIERS = '''
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python :: 2
Programming Language :: Python :: 3
'''.strip().splitlines()
CURDIR = dirname(abspath(__file__))
with open(join(CURDIR, NAME + '.py')) as source:
    VERSION = re.search("\n__version__ = '(.*)'", source.read()).group(1)
with open(join(CURDIR, 'README.rst')) as readme:
    README = readme.read()
with open(join(CURDIR, 'requirements.txt')) as requirements:
    REQUIREMENTS = requirements.read().splitlines()
ENTRY_POINTS = '''
[pygments.lexers]
robotframework = robotframeworklexer:RobotFrameworkLexer
'''

setup(
    name         = NAME,
    version      = VERSION,
    description  = __doc__,
    long_description = open('README.rst').read(),
    author       = u'Pekka Kl\xe4rck',
    author_email = 'peke@iki.fi',
    license      = 'Apache License 2.0',
    url          = 'https://github.com/robotframework/pygmentslexer',
    download_url = 'https://pypi.org/project/robotframeworklexer',
    keywords     = 'pygments robotframework',
    platforms    = 'any',
    py_modules   = [NAME],
    entry_points = ENTRY_POINTS,
    requires     = REQUIREMENTS
)
