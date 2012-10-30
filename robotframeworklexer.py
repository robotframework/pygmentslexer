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


class Variable(object):
    _space_splitter = re.compile('( {2,})')
    _pipe_splitter = re.compile('( +\| +)')
    _pipe_start = re.compile('(^\| +)')
    _pipe_end = re.compile('( +\| *\n)')
    _types = [VARIABLE, ARGUMENT]

    def __init__(self, pipes=False):
        if not pipes:
            self._splitter = self._split_from_spaces
            self._index_adjust = 0
            self._separator = SPACES
        else:
            self._splitter = self._split_from_pipes
            self._index_adjust = -1
            self._separator = PIPE

    def __call__(self, lexer, match):
        position = 0
        commented = False
        for index, token in enumerate(self._splitter(match.group(0))):
            commented = commented or token.startswith('#')
            type = self._get_type(index, commented)
            yield (position, type, token)
            position += len(token)

    def _get_type(self, index, commented):
        if commented:
            return COMMENT
        index += self._index_adjust
        if not index % 2:
            return self._separator
        if index > len(self._types):
            return self._types[-1]
        return self._types[index]

    def _split_from_spaces(self, row):
        for token in self._space_splitter.split(row):
            yield token

    def _split_from_pipes(self, row):
        _, start, row = self._pipe_start.split(row)
        yield start
        if self._pipe_end.search(row):
            row, end, _ = self._pipe_end.split(row)
        else:
            end = None
        for token in self._pipe_splitter.split(row):
            yield token
        if end:
            yield end


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
            include('empty-row'),
            (r'\*', HEADING, '#pop'),
            (r'\| .*\n', Variable(pipes=True)),
            (r'.*\n', Variable()),
        ],
        'tests': [
            include('comment'),
            (r'^\S.*?(\n|  +)', Generic.Subheading),
            (r'^ +', Text),
            (r'.*\n', Keyword)
        ]
    }
