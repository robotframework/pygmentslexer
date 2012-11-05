#  Copyright 2012 Nokia Siemens Networks Oyj
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
SETTING = Keyword.Namespace
IMPORT = Name.Namespace
NAME = Generic.Subheading
KEYWORD = Name.Function
ARGUMENT = String
VAR_BASE = Name
VAR_DECO = Name.Variable
COMMENT = Comment
SEPARATOR = Punctuation
SYNTAX = Punctuation
ERROR = Error


class RobotFrameworkLexer(Lexer):
    name = 'RobotFrameworkLexer'
    aliases = ['robotframework']
    filenames = ['*.txt']

    def __init__(self):
        Lexer.__init__(self, tabsize=2, encoding='UTF-8')

    def get_tokens_unprocessed(self, text):
        row_tokenizer = RowTokenizer()
        var_tokenizer = VariableTokenizer()
        position = 0
        for row in text.splitlines():
            for token, type in row_tokenizer.tokenize(row):
                for token, type in var_tokenizer.tokenize(token, type):
                    if token:
                        yield position, type, unicode(token)
                        position += len(token)


class VariableTokenizer(object):

    def tokenize(self, string, type):
        var = VariableSplitter(string, identifiers='$@%')
        if var.start < 0 or type is COMMENT:
            yield string, type
            return
        for token, type in self._tokenize(var, string, type):
            if token:
                yield token, type

    def _tokenize(self, var, string, orig_type):
        before = string[:var.start]
        yield before, orig_type
        yield var.identifier + '{', VAR_DECO
        for token, type in self.tokenize(var.base, VAR_BASE):
            yield token, type
        yield '}', VAR_DECO
        if var.index:
            yield '[', VAR_DECO
            for token, type in self.tokenize(var.index, VAR_BASE):
                yield token, type
            yield ']', VAR_DECO
        for token, type in self.tokenize(string[var.end:], orig_type):
            yield token, type


class RowTokenizer(object):

    def __init__(self):
        self._table = UnknownTable()
        self._splitter = Splitter()
        settings = SettingTable()
        variables = VariableTable()
        testcases = TestCaseTable()
        keywords = KeywordTable()
        self._tables = {'settings': settings,
                        'setting': settings,
                        'metadata': settings,
                        'variables': variables,
                        'variable': variables,
                        'testcases': testcases,
                        'testcase': testcases,
                        'keywords': keywords,
                        'keyword': keywords,
                        'userkeywords': keywords,
                        'userkeyword': keywords}

    def tokenize(self, row):
        commented = False
        heading = False
        for index, token in enumerate(self._splitter.split(row)):
            # First token, and every second after that, is a separator.
            index, separator = divmod(index-1, 2)
            if token.startswith('#'):
                commented = True
            elif index == 0 and token.startswith('*'):
                self._table = self._start_table(token)
                heading = True
            for token, type in self._tokenize(token, index, commented, separator, heading):
                yield token, type
        self._table.end_row()

    def _start_table(self, header):
        name = header.replace('*', '').replace(' ', '').lower()
        return self._tables.get(name, UnknownTable())

    def _tokenize(self, token, index, commented, separator, heading):
        if commented:
            yield token, COMMENT
        elif separator:
            yield token, SEPARATOR
        elif heading:
            yield token, HEADING
        else:
            for token, type in self._table.tokenize(token, index):
                yield token, type


class Splitter(object):
    _space_splitter = re.compile('( {2,})')
    _pipe_splitter = re.compile('( +\| +)')
    _pipe_start = re.compile('^(\| +)')
    _pipe_end = re.compile('( +\|)$')

    def split(self, row):
        for token in self._split(row.rstrip()):
            yield token
        yield '\n'

    def _split(self, row):
        if self._pipe_start.match(row):
            return self._split_from_pipes(row)
        return self._split_from_spaces(row)

    def _split_from_spaces(self, row):
        yield ''  # Start with (pseudo)separator similarly as with pipes
        for token in self._space_splitter.split(row):
            yield token

    def _split_from_pipes(self, row):
        _, start, row = self._pipe_start.split(row)
        yield start
        if self._pipe_end.search(row):
            row, end, _ = self._pipe_end.split(row)
        else:
            end = ''
        for token in self._pipe_splitter.split(row):
            yield token
        yield end


class TypeGetter(object):
    _types = None

    def __init__(self):
        self._index = 0

    def tokenize(self, token):
        tokens_and_types = self._tokenize(token, self._index)
        self._index += 1
        if not isinstance(tokens_and_types, list):
            tokens_and_types = [(token, tokens_and_types)]
        return tokens_and_types

    def _tokenize(self, token, index):
        index = min(index, len(self._types) - 1)
        return self._types[index]


class Comment(TypeGetter):
    _types = [COMMENT]


class Setting(TypeGetter):
    _types = [SETTING, ARGUMENT]
    _keyword_settings = ('suitesetup',
                         'suiteprecondition',
                         'suiteteardown',
                         'suitepostcondition',
                         'testsetup',
                         'testprecondition',
                         'testteardown',
                         'testpostcondition',
                         'testtemplate')
    _import_settings = ('library',
                        'resource',
                        'variables')
    _other_settings = ('documentation',
                       'metadata',
                       'forcetags',
                       'defaulttags',
                       'testtimeout')
    _custom_tokenizer = None

    def _tokenize(self, token, index):
        if index == 0:
            normalized = token.lower().replace(' ', '')
            if normalized in self._keyword_settings:
                self._custom_tokenizer = KeywordCall(support_assign=False)
            elif normalized in self._import_settings:
                self._custom_tokenizer = ImportSetting()
            elif normalized not in self._other_settings:
                return ERROR
        elif self._custom_tokenizer:
            return self._custom_tokenize(token, index)
        return TypeGetter._tokenize(self, token, index)

    def _custom_tokenize(self, token, index):
        return self._custom_tokenizer.tokenize(token)


class ImportSetting(TypeGetter):
    _types = [IMPORT, ARGUMENT]


class TestCaseSetting(Setting):
    _keyword_settings = ('setup',
                         'precondition',
                         'teardown',
                         'postcondition',
                         'template')
    _import_settings = ()
    _other_settings = ('documentation',
                       'tags',
                       'timeout')

    def _tokenize(self, token, index):
        if index == 0:
            type = Setting._tokenize(self, token[1:-1], index)
            return [('[', SYNTAX), (token[1:-1], type), (']', SYNTAX)]
        return Setting._tokenize(self, token, index)


class TemplateSetting(TestCaseSetting):

    def __init__(self, set_template):
        TestCaseSetting.__init__(self)
        self._set_template = set_template

    def _custom_tokenize(self, token, index):
        if index == 1:
            self._set_template(token)
        return self._custom_tokenizer.tokenize(token)


class KeywordSetting(TestCaseSetting):
    _keyword_settings = ('teardown',)
    _other_settings = ('documentation',
                       'arguments',
                       'return',
                       'timeout')


class Variable(TypeGetter):
    _types = [VAR_BASE, ARGUMENT]


class KeywordCall(TypeGetter):
    _types = [KEYWORD, ARGUMENT]

    def __init__(self, support_assign=True):
        TypeGetter.__init__(self)
        self._keyword_found = not support_assign
        self._assigns = 0

    def _tokenize(self, token, index):
        if not self._keyword_found and self._is_assign(token):
            self._assigns += 1
            return SYNTAX  # VariableTokenizer tokenizes this later.
        self._keyword_found = True
        return TypeGetter._tokenize(self, token, index - self._assigns)

    def _is_assign(self, token):
        return token.startswith(('${', '@{')) and token.rstrip(' =').endswith('}')


class TemplatedKeywordCall(TypeGetter):
    _types = [ARGUMENT]


class ForLoop(TypeGetter):

    def __init__(self):
        TypeGetter.__init__(self)
        self._in_arguments = False

    def _tokenize(self, token, index):
        type = ARGUMENT if self._in_arguments else SYNTAX
        if token.upper() in ['IN', 'IN RANGE']:
            self._in_arguments = True
        return type


class _Table(object):
    _type_getter_class = None

    def __init__(self, prev_type_getter=None):
        self._type_getter = self._type_getter_class()
        self._prev_type_getter = prev_type_getter
        self._prev_tokens_in_row = []

    def tokenize(self, token, index):
        if self._continues(token, index):
            self._type_getter = self._prev_type_getter
            yield token, SYNTAX
        else:
            for token_and_type in self._tokenize(token, index):
                yield token_and_type
        self._prev_tokens_in_row.append(token)

    def _continues(self, token, index):
        return token == '...' \
                and all(self._is_empty(t) for t in self._prev_tokens_in_row)

    def _is_empty(self, token):
        return token in ['', '\\']

    def _tokenize(self, token, index):
        return self._type_getter.tokenize(token)

    def end_row(self):
        self.__init__(prev_type_getter=self._type_getter)


class UnknownTable(_Table):
    _type_getter_class = Comment

    def _continues(self, token, index):
        return False


class VariableTable(_Table):
    _type_getter_class = Variable


class SettingTable(_Table):
    _type_getter_class = Setting


class TestCaseTable(_Table):
    _setting_getter_class = TestCaseSetting
    _test_template = False

    @property
    def _type_getter_class(self):
        if self._test_template:
            return TemplatedKeywordCall
        return KeywordCall

    def _continues(self, token, index):
        return index > 0 and _Table._continues(self, token, index)

    def _tokenize(self, token, index):
        if index == 0:
            if token:
                self._test_template = False
            return [(token, NAME)]
        if index == 1 and self._is_setting(token):
            if self._is_template(token):
                self._type_getter = TemplateSetting(self._set_template)
            else:
                self._type_getter = self._setting_getter_class()
        if index == 1 and self._is_for_loop(token):
            self._type_getter = ForLoop()
        if index == 1 and self._is_empty(token):
            return [(token, SYNTAX)]
        return _Table._tokenize(self, token, index)

    def _is_setting(self, token):
        return token.startswith('[') and token.endswith(']')

    def _is_template(self, token):
        return token.upper().replace(' ', '') == '[TEMPLATE]'

    def _is_for_loop(self, token):
        return token.startswith(':') and \
                token.upper().replace(':', '').strip() == 'FOR'

    def _set_template(self, template):
        self._test_template = template.upper() not in ('', '\\', 'NONE', '${EMPTY}')


class KeywordTable(TestCaseTable):
    _type_getter_class = KeywordCall
    _setting_getter_class = KeywordSetting

    def _is_template(self, token):
        return False


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
