#!/usr/bin/env python

"""Pygments lexer for Robot Framework test data."""

from setuptools import setup


entry_points = '''
[pygments.lexers]
robotframework = robotframeworklexer:RobotFrameworkLexer
'''

setup(
    name         = 'robotframeworklexer',
    version      = '1.0',
    description  = __doc__,
    long_description = open('README.rst').read(),
    author       = 'Robot Framework Developers',
    author_email = 'robotframework-devel@googlegroups.com',
    license      = 'Apache License 2.0',
    url          = 'https://bitbucket.org/pekkaklarck/robotframeworklexer',
    download_url = 'https://bitbucket.org/pekkaklarck/robotframeworklexer/downloads',
    keywords     = 'pygments robotframework',
    platforms    = 'any',
    py_modules   = ['robotframeworklexer'],
    entry_points = entry_points,
    requires     = ['pygments']
)
