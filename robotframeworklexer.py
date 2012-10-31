import re

from pygments.lexer import Lexer
from pygments.token import *


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
    _types = None

    def get(self, token, index):
        index = index if index < len(self._types) else -1
        return self._types[index]

    def end_of_line(self):
        pass


class Variable(TypeGetter):
    _types = [VARIABLE, ARGUMENT]


class Setting(TypeGetter):
    _types = [SETTING, ARGUMENT]


class TestCase(TypeGetter):
    _types = [NAME, KW_NAME, ARGUMENT]

    def __init__(self):
        self._assign = []
        self._keyword_found = False

    def get(self, token, index):
        if index == 0:
            return TypeGetter.get(self, token, index)
        if index == 1 and token.startswith('[') and token.endswith(']'):
            return SETTING
        if not self._keyword_found and \
            token.startswith(('${', '@{')) and token.rstrip(' =').endswith('}'):
            self._assign.append(token)
            return VARIABLE
        else:
            self._keyword_found = True
        return TypeGetter.get(self, token, index - len(self._assign))

    def end_of_line(self):
        self.__init__()


class Keyword(TestCase):
    pass


class Splitter(object):
    _space_splitter = re.compile('( {2,})')
    _pipe_splitter = re.compile('( +\| +)')
    _pipe_start = re.compile('(^\| +)')
    _pipe_end = re.compile('( +\| *\n)')

    def split(self, row, pipes=False):
        if pipes:
            return self.split_from_pipes(row)
        return self.split_from_spaces(row)

    def split_from_spaces(self, row):
        for token in self._space_splitter.split(row):
            yield token

    def split_from_pipes(self, row):
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


class RobotFrameworkLexer(Lexer):
    flags = re.IGNORECASE | re.MULTILINE
    name = 'RobotFrameworkLexer'
    aliases = ['robotframework']
    filenames = ['*.txt']

    def __init__(self):
        Lexer.__init__(self, tabsize=2, encoding='UTF-8')

    def get_tokens_unprocessed(self, text):
        type_getter = None
        splitter = Splitter()
        position = 0   # Who uses this???
        var_finder = VariableFinder()
        for line in text.splitlines(True):
            pipes = line.startswith('| ')
            commented = False
            for index, token in enumerate(splitter.split(line, pipes)):
                index, separator = divmod(index - (1 if pipes else 0), 2)
                commented = commented or token.startswith('#')
                if commented:
                    yield (position, COMMENT, token)
                elif separator:
                    yield (position, PIPE, token)
                elif index == 0 and token.startswith('*'):
                    table = token.strip().strip('*').replace(' ', '').rstrip('s').lower()
                    type_getter = {'setting': Setting(),
                              'variable': Variable(),
                              'testcase': TestCase(),
                              'keyword': Keyword()}[table]
                    yield (position, HEADING, token)
                else:
                    type = type_getter.get(token, index)
                    for token, type in var_finder.tokenize(token, type):
                        yield (position, type, token)
            type_getter.end_of_line()
