import re

from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import *


TODO = Generic.Heading
HEADING = Generic.Heading
SETTING = Generic.Subheading
VARIABLE = Name.Variable
ARGUMENT = Name
COMMENT = Comment
PIPE = Generic.Heading
SPACES = Text

SPACE_SEP = r'(?: {2,}|\t+)'
PIPE_SEP = r' +\| +'


class RobotFrameworkLexer(RegexLexer):
    flags = re.IGNORECASE | re.MULTILINE
    name = 'RobotFrameworkLexer'
    aliases = ['robotframework']
    filenames = ['*.txt']

    tokens = {
        'comment': [
            (r' *#.*\n', COMMENT),
        ],
        'empty-row': [
            (r'^\n', SPACES),
        ],
        'generic': [
            include('comment'),
            include('empty-row')
        ],
        'root': [
            include('generic'),
            (r'\*[\* ]*Settings?[\* ]*\n', HEADING, 'settings'),
            (r'\*[\* ]*Variables?[\* ]*\n', HEADING, 'variables'),
            (r'\*[\* ]*Test ?Cases?[\* ]*\n', HEADING, 'tests'),
        ],
        'settings': [
            include('generic'),
            (r'\*', HEADING, '#pop'),
            (r'(.+?)(( {2,}|\t).*\n)', bygroups(SETTING, ARGUMENT)),
        ],
        'variables': [
            include('generic'),
            (r'\*', HEADING, '#pop'),
            (r'[^\|].*?(?= {2,})', VARIABLE, 'spaces'),
            (r'^(\| +)(.*?)(?= +\|)', bygroups(PIPE, VARIABLE), 'pipes')
        ],
        'spaces': [
            (r' *\n', SPACES, '#pop'),
            (r'#.*\n', COMMENT, '#pop'),
            (r' {2,}', SPACES),
            (r'.+?(?= {2,}|\n)', ARGUMENT),
        ],
        'pipes': [
            (r'( +\|)? *\n', PIPE, '#pop'),
            (r'#.*\n', COMMENT, '#pop'),
            (r' +\| +', PIPE),
            (r'.+?(?= +\| +)', ARGUMENT),
            (r'.+?(?=( +\|)? *$)', ARGUMENT),
        ],
        'tests': [
            include('comment'),
            (r'^\S.*?(\n|  +)', Generic.Subheading),
            (r'^ +', Text),
            (r'.*\n', Keyword)
        ]
    }
