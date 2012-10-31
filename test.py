#!/usr/bin/env python

from pygments import highlight
from pygments.formatters import HtmlFormatter

from robotframeworklexer import RobotFrameworkLexer


inpath = 'tests.txt'
outpath = 'tests.html'

with open(inpath) as infile:
    with open(outpath, 'w') as outfile:
        formatter = HtmlFormatter(full=True, style='autumn', encoding='UTF-8')
        highlight(infile.read(), RobotFrameworkLexer(), formatter, outfile)

print outpath
