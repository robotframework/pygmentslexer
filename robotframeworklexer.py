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


class Types(object):

    def __init__(self, types, pipes=False):
        self._types = types
        if not pipes:
            self._index_adjust = 0
            self._separator = SPACES
        else:
            self._index_adjust = -1
            self._separator = PIPE
        self._commented = False

    def get(self, index, token):
        self._commented = self._commented or token.startswith('#')
        if self._commented:
            return COMMENT
        index += self._index_adjust
        if index % 2:
            return self._separator
        if index < len(self._types):
            return self._types[index]
        return self._types[-1]


class Splitter(object):
    _space_splitter = re.compile('( {2,})')
    _pipe_splitter = re.compile('( +\| +)')
    _pipe_start = re.compile('(^\| +)')
    _pipe_end = re.compile('( +\| *\n)')

    def __init__(self, pipes=False):
        self.split = self._from_spaces if not pipes else self._from_pipes

    def _from_spaces(self, row):
        for token in self._space_splitter.split(row):
            yield token

    def _from_pipes(self, row):
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


class Variable(object):
    _types = [VARIABLE, ARGUMENT]

    def __init__(self, pipes=False):
        self._pipes = pipes

    def __call__(self, lexer, match):
        row = match.group(0)
        pipes = row.startswith('| ')
        types = Types(self._types, pipes)
        splitter = Splitter(pipes)
        position = 0
        for index, token in enumerate(splitter.split(row)):
            yield (position, types.get(index, token), token)
            position += len(token)


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
            (r'.*\n', Variable()),
        ],
        'tests': [
            include('comment'),
            (r'^\S.*?(\n|  +)', Generic.Subheading),
            (r'^ +', Text),
            (r'.*\n', Keyword)
        ]
    }
