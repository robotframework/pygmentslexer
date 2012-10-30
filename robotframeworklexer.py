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
NAME = Generic.Subheading
KW_NAME = Name.Function


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
        index, modulo = divmod(index + self._index_adjust, 2)
        if modulo:
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


class VariableFinder(object):
    _start = re.compile(r'(\$\{)')
    _end = '}'

    def tokenize(self, string, type):
        # TODO: cleanup, enhance, and unit test
        if not self._start.search(string):
            yield string, type
            raise StopIteration
        before, start, after = self._start.split(string, 1)
        if '}' not in after:
            yield string, type
        yield before, type
        base, after = after.split('}', 1)
        yield start + base + '}', VARIABLE
        for token, type in self.tokenize(after, type):
            yield token, type




class RowParser(object):
    _types = None

    def __call__(self, lexer, match):
        row = match.group(0)
        return iter(self.tokenize(row, pipes=row.startswith('| ')))

    def tokenize(self, row, pipes=False):
        types = Types(self._types, pipes)
        splitter = Splitter(pipes)
        var_finder = VariableFinder()
        position = 0
        for index, token in enumerate(splitter.split(row)):
            type = types.get(index, token)
            for token, type in var_finder.tokenize(token, type):
                yield (position, type, token)
                position += len(token)


class Variable(RowParser):
    _types = [VARIABLE, ARGUMENT]


class Setting(RowParser):
    _types = [SETTING, ARGUMENT]


class TestCase(RowParser):
    _types = [NAME, KW_NAME, ARGUMENT]



class RobotFrameworkLexer(RegexLexer):
    flags = re.IGNORECASE | re.MULTILINE
    name = 'RobotFrameworkLexer'
    aliases = ['robotframework']
    filenames = ['*.txt']

    tokens = {
        'root': [
            include('generic'),
            (r'\*[\* ]*Settings?[\* ]*\n', HEADING, 'settings'),
            (r'\*[\* ]*Variables?[\* ]*\n', HEADING, 'variables'),
            (r'\*[\* ]*Test ?Cases?[\* ]*\n', HEADING, 'tests'),
        ],
        'settings': [
            include('pop-heading'),
            (r'.*\n', Setting()),
        ],
        'variables': [
            include('pop-heading'),
            (r'.*\n', Variable()),
        ],
        'tests': [
            include('pop-heading'),
            (r'.*\n', TestCase())
        ],
        'generic': [
            (r' *#.*\n', COMMENT),
            (r'^\n', SPACES),
        ],
        'pop-heading': [
            (r'(?=\*)', HEADING, '#pop')
        ],
    }
