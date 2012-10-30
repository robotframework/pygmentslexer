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


class TypeGetter(object):

    def __init__(self, types, pipes=False):
        self._types = types
        self._separator, self._index_adjust = (PIPE, -1) if pipes else (SPACES, 0)
        self._commented = False

    def get(self, token, index):
        self._commented = self._commented or token.startswith('#')
        if self._commented:
            return COMMENT
        index, modulo = divmod(index + self._index_adjust, 2)
        if modulo:
            return self._separator
        return self._get(token, index)

    def _get(self, token, index):
        index = index if index < len(self._types) else -1
        return self._types[index]


class TestCaseTypeGetter(TypeGetter):

    def __init__(self, pipes=False):
        TypeGetter.__init__(self, [NAME, KW_NAME, ARGUMENT], pipes)
        self._assign = []
        self._keyword_found = False

    def _get(self, token, index):
        if index == 0:
            return TypeGetter._get(self, token, index)
        if index == 1 and token.startswith('[') and token.endswith(']'):
            return SETTING
        if not self._keyword_found and \
            token.startswith(('${', '@{')) and token.rstrip(' =').endswith('}'):
            self._assign.append(token)
            return VARIABLE
        else:
            self._keyword_found = True
        return TypeGetter._get(self, token, index - len(self._assign))



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
        if not self._start.search(string) or type is VARIABLE:
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

    def __call__(self, lexer, match):
        row = match.group(0)
        return iter(self.tokenize(row, pipes=row.startswith('| ')))

    def tokenize(self, row, pipes=False):
        types = self._type_getter(pipes)
        splitter = Splitter(pipes)
        var_finder = VariableFinder()
        position = 0
        for index, token in enumerate(splitter.split(row)):
            type = types.get(token, index)
            for token, type in var_finder.tokenize(token, type):
                yield (position, type, token)
                position += len(token)

    def _type_getter(self, pipes):
        raise NotImplementedError



class Variable(RowParser):

    def _type_getter(self, pipes):
        return TypeGetter([VARIABLE, ARGUMENT], pipes)


class Setting(RowParser):

    def _type_getter(self, pipes):
        return TypeGetter([SETTING, ARGUMENT], pipes)


class TestCase(RowParser):

    def _type_getter(self, pipes):
        return TestCaseTypeGetter(pipes)


class Keyword(RowParser):

    def _type_getter(self, pipes):
        return TestCaseTypeGetter(pipes)


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
            (r'\*[\* ]*Keywords?[\* ]*\n', HEADING, 'keywords'),
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
        'keywords': [
            include('pop-heading'),
            (r'.*\n', Keyword())
        ],
        'generic': [
            (r' *#.*\n', COMMENT),
            (r'^\n', SPACES),
        ],
        'pop-heading': [
            (r'(?=\*)', HEADING, '#pop')
        ],
    }
