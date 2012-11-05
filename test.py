#!/usr/bin/env python

import sys
from pygments import highlight
from pygments.formatters import HtmlFormatter

from robotframeworklexer import RobotFrameworkLexer


inpath = 'tests.txt' if len(sys.argv) < 2 else sys.argv[1]
outpath = 'out.html'
style = 'autumn' if len(sys.argv) < 3 else sys.argv[2]

with open(inpath) as infile:
    with open(outpath, 'w') as outfile:
        formatter = HtmlFormatter(full=True, style=style, encoding='UTF-8')
        highlight(infile.read(), RobotFrameworkLexer(), formatter, outfile)

print outpath
