import re

from pygments.lexer import RegexLexer, bygroups
from pygments.token import *


TODO = Generic.Heading

HEADING = Generic.Heading
SETTING = Generic.Emph
ARGUMENTS = Generic.Subheading

class RobotFrameworkLexer(RegexLexer):
    flags = re.IGNORECASE|re.MULTILINE
    name = 'RobotFrameworkLexer'
    aliases = ['robotframework']
    filenames = ['*.txt']

    tokens = {
        'root': [
            (r'\*[\* ]*Settings?[\* ]*\n', HEADING, 'settings'),
            (r'\*[\* ]*Test ?Cases?[\* ]*\n', HEADING, 'tests'),
        ],
        'settings': [
            (r'\*', HEADING, '#pop'),
            (r'(.+?)(( {2,}|\t).*\n)', bygroups(SETTING, ARGUMENTS)),
        ],
        'tests': [
            (r'^\S.*?(\n|  +)', Generic.Subheading),
            (r'^ +', Text),
            (r'.*\n', Keyword)
        ]
    }
