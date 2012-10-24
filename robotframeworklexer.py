import re

from pygments.lexer import RegexLexer
from pygments.token import *


TODO = Generic.Heading

class RobotFrameworkLexer(RegexLexer):
    flags = re.IGNORECASE|re.MULTILINE
    name = 'RobotFrameworkLexer'
    aliases = ['robotframework']
    filenames = ['*.txt']

    tokens = {
        'root': [
            (r'\*[\* ]*Settings?[\* ]*\n', Generic.Heading, 'settings'),
            (r'\*[\* ]*Test ?Cases?[\* ]*\n', Generic.Heading, 'tests'),
        ],
        'settings': [
            (r'Library.*\n', Generic.Emph, '#pop'),
        ],
        'tests': [
            (r'^\S.*?(\n|  +)', Generic.Subheading),
            (r'^ +', Text),
            (r'.*\n', Keyword)
        ]
    }
