#!/usr/bin/env python

"""Pygments lexer for Robot Framework test data."""

from setuptools import setup


entry_points = '''
[pygments.lexers]
robotframework = robotframeworklexer:RobotFrameworkLexer
'''

setup(
    name         = 'robotframeworklexer',
    version      = 'dev',
    description  = __doc__,
    long_description = open('README.rst').read(),
    author       = u'Pekka Kl\xe4rck',
    author_email = 'peke@iki.fi',
    license      = 'Apache License 2.0',
    url          = 'https://github.com/robotframework/pygmentslexer',
    download_url = 'https://pypi.org/project/robotframeworklexer',
    keywords     = 'pygments robotframework',
    platforms    = 'any',
    py_modules   = ['robotframeworklexer'],
    entry_points = entry_points,
    requires     = ['pygments']
)
