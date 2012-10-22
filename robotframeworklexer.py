import re

from pygments.lexer import RegexLexer
from pygments.token import *


class RobotFrameworkLexer(RegexLexer):
    flags = re.IGNORECASE
    name = 'RobotFrameworkLexer'
    aliases = ['robotframework']
    filenames = ['*.txt']

    tokens = {
        'root': [
            (r'\*[\* ]*Settings?[\* ]*\n', Generic.Heading, 'settings'),
            (r'.*\n', Text),
        ],
        'settings': [
            (r'Library.*\n', Generic.Emph),
        ]
    }
