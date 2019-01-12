#!/usr/bin/env python

"""Usage: generate.py inpath [outpath=out.html] [style=autumn]"""

import sys
from pygments import highlight
from pygments.formatters import HtmlFormatter
from robotframeworklexer import RobotFrameworkLexer


def generate(inpath, outpath='out.html', style='autumn'):
    with open(inpath) as infile:
        with open(outpath, 'wb') as outfile:
            formatter = HtmlFormatter(full=True, style=style, encoding='UTF-8')
            highlight(infile.read(), RobotFrameworkLexer(), formatter, outfile)
    return outpath


if __name__ == '__main__':
    if 2 <= len(sys.argv) <= 4:
        print(generate(*sys.argv[1:]))
    else:
        sys.exit(__doc__)
