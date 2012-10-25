import re

from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import *


TODO = Generic.Heading
HEADING = Generic.Heading
SETTING = Generic.Emph
ARGUMENTS = Generic.Subheading
COMMENT = Comment.Single


class RobotFrameworkLexer(RegexLexer):
    flags = re.IGNORECASE | re.MULTILINE
    name = 'RobotFrameworkLexer'
    aliases = ['robotframework']
    filenames = ['*.txt']

    tokens = {
        'comment': [
            (r'#.*?\n', COMMENT)
        ],
        'root': [
            include('comment'),
            (r'\*[\* ]*Settings?[\* ]*\n', HEADING, 'settings'),
            (r'\*[\* ]*Test ?Cases?[\* ]*\n', HEADING, 'tests'),
        ],
        'settings': [
            include('comment'),
            (r'\*', HEADING, '#pop'),
            (r'(.+?)(( {2,}|\t).*\n)', bygroups(SETTING, ARGUMENTS)),
        ],
        'tests': [
            include('comment'),
            (r'^\S.*?(\n|  +)', Generic.Subheading),
            (r'^ +', Text),
            (r'.*\n', Keyword)
        ]
    }
