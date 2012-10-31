#  Copyright 2008-2012 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import re

from pygments.lexer import Lexer
from pygments.token import *


HEADING = Generic.Heading
SETTING = Generic.Subheading
VAR_BASE = Name
VAR_DECO = Name.Variable
ARGUMENT = Name
COMMENT = Comment
SEPARATOR = Generic.Heading
NAME = Generic.Subheading
KW_NAME = Name.Function
SYNTAX = Name


class TypeGetter(object):
    _types = None

    def get(self, token, index):
        index = index if index < len(self._types) else -1
        return self._types[index]

    def end_of_line(self):
        pass


class Variable(TypeGetter):
    _types = [VAR_BASE, ARGUMENT]


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
            return SYNTAX  # VariableFinder tokenizes this later
        else:
            self._keyword_found = True
        return TypeGetter.get(self, token, index - len(self._assign))

    def end_of_line(self):
        self.__init__()


class Comment(TypeGetter):
    _types = [COMMENT]


class Keyword(TestCase):
    pass


class Splitter(object):
    _space_splitter = re.compile('( {2,})')
    _pipe_splitter = re.compile('( +\| +)')
    _pipe_start = re.compile('^(\| +)')
    _pipe_end = re.compile('( +\| *\n)')

    def split(self, row):
        if self._pipe_start.match(row):
            return self._split_from_pipes(row)
        return self._split_from_spaces(row)

    def _split_from_spaces(self, row):
        yield u''  # Yield elements same way as when pipe is separator
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


class VariableTokenizer(object):
    _start = re.compile(r'(\\*[$@]\{)')
    _end = u'}'

    def tokenize(self, string, type):
        # TODO: cleanup, enhance, and unit test
        if not self._start.search(string):
            yield string, type
            return
        before, start, after = self._start.split(string, 1)
        if self._end not in after:
            yield string, type
            return
        if before:
            yield before, type
        base, after = after.split(self._end, 1)
        yield start, VAR_DECO
        yield base, VAR_BASE
        yield self._end, VAR_DECO
        for token, type in self.tokenize(after, type):
            if token:
                yield token, type


class RobotFrameworkLexer(Lexer):
    name = 'RobotFrameworkLexer'
    aliases = ['robotframework']
    filenames = ['*.txt']

    def __init__(self):
        Lexer.__init__(self, tabsize=2, encoding='UTF-8')

    def get_tokens_unprocessed(self, text):
        types = Comment()
        splitter = Splitter()
        position = 0   # Who uses this???
        var_tokenizer = VariableTokenizer()
        for line in text.splitlines(True):
            commented = False
            for index, token in enumerate(splitter.split(line)):
                index, separator = divmod(index-1, 2)
                commented = commented or token.startswith('#')
                if commented:
                    yield (position, COMMENT, token)
                elif separator:
                    yield (position, SEPARATOR, token)
                elif index == 0 and token.startswith('*'):
                    table = token.strip().strip('*').replace(' ', '').rstrip('s').lower()
                    types = {'setting': Setting(),
                             'variable': Variable(),
                             'testcase': TestCase(),
                             'keyword': Keyword()}.get(table, Comment())
                    yield (position, HEADING, token)
                else:
                    type = types.get(token, index)
                    for token, type in var_tokenizer.tokenize(token, type):
                        yield (position, type, token)
            types.end_of_line()


# Following code copied directly from Robot Framework 2.7.5.

class VariableSplitter:

    def __init__(self, string, identifiers):
        self.identifier = None
        self.base = None
        self.index = None
        self.start = -1
        self.end = -1
        self._identifiers = identifiers
        self._may_have_internal_variables = False
        try:
            self._split(string)
        except ValueError:
            pass
        else:
            self._finalize()

    def get_replaced_base(self, variables):
        if self._may_have_internal_variables:
            return variables.replace_string(self.base)
        return self.base

    def _finalize(self):
        self.identifier = self._variable_chars[0]
        self.base = ''.join(self._variable_chars[2:-1])
        self.end = self.start + len(self._variable_chars)
        if self._has_list_variable_index():
            self.index = ''.join(self._list_variable_index_chars[1:-1])
            self.end += len(self._list_variable_index_chars)

    def _has_list_variable_index(self):
        return self._list_variable_index_chars\
        and self._list_variable_index_chars[-1] == ']'

    def _split(self, string):
        start_index, max_index = self._find_variable(string)
        self.start = start_index
        self._open_curly = 1
        self._state = self._variable_state
        self._variable_chars = [string[start_index], '{']
        self._list_variable_index_chars = []
        self._string = string
        start_index += 2
        for index, char in enumerate(string[start_index:]):
            index += start_index  # Giving start to enumerate only in Py 2.6+
            try:
                self._state(char, index)
            except StopIteration:
                return
            if index  == max_index and not self._scanning_list_variable_index():
                return

    def _scanning_list_variable_index(self):
        return self._state in [self._waiting_list_variable_index_state,
                               self._list_variable_index_state]

    def _find_variable(self, string):
        max_end_index = string.rfind('}')
        if max_end_index == -1:
            return ValueError('No variable end found')
        if self._is_escaped(string, max_end_index):
            return self._find_variable(string[:max_end_index])
        start_index = self._find_start_index(string, 1, max_end_index)
        if start_index == -1:
            return ValueError('No variable start found')
        return start_index, max_end_index

    def _find_start_index(self, string, start, end):
        index = string.find('{', start, end) - 1
        if index < 0:
            return -1
        if self._start_index_is_ok(string, index):
            return index
        return self._find_start_index(string, index+2, end)

    def _start_index_is_ok(self, string, index):
        return string[index] in self._identifiers\
        and not self._is_escaped(string, index)

    def _is_escaped(self, string, index):
        escaped = False
        while index > 0 and string[index-1] == '\\':
            index -= 1
            escaped = not escaped
        return escaped

    def _variable_state(self, char, index):
        self._variable_chars.append(char)
        if char == '}' and not self._is_escaped(self._string, index):
            self._open_curly -= 1
            if self._open_curly == 0:
                if not self._is_list_variable():
                    raise StopIteration
                self._state = self._waiting_list_variable_index_state
        elif char in self._identifiers:
            self._state = self._internal_variable_start_state

    def _is_list_variable(self):
        return self._variable_chars[0] == '@'

    def _internal_variable_start_state(self, char, index):
        self._state = self._variable_state
        if char == '{':
            self._variable_chars.append(char)
            self._open_curly += 1
            self._may_have_internal_variables = True
        else:
            self._variable_state(char, index)

    def _waiting_list_variable_index_state(self, char, index):
        if char != '[':
            raise StopIteration
        self._list_variable_index_chars.append(char)
        self._state = self._list_variable_index_state

    def _list_variable_index_state(self, char, index):
        self._list_variable_index_chars.append(char)
        if char == ']':
            raise StopIteration
