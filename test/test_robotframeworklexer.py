import unittest

from robotframeworklexer import *


class TestVariableTokenizer(unittest.TestCase):

    def _verify(self, string, *expected):
        tokenizer = VariableTokenizer()
        actual = list(tokenizer.tokenize(string, ARGUMENT))
        self.assertEqual(len(actual), len(expected))
        for act, exp in zip(actual, expected):
            self.assertEqual(act, exp)

    def test_empty_string(self):
        self._verify('', ('', ARGUMENT))

    def test_no_variable(self):
        self._verify('text', ('text', ARGUMENT))
        self._verify('${text', ('${text', ARGUMENT))

    def test_scalar_variable(self):
        self._verify('${variable}',
                     ('${', SYNTAX), ('variable', VARIABLE), ('}', SYNTAX))

    def test_list_variable(self):
        self._verify('@{my var}',
                     ('@{', SYNTAX), ('my var', VARIABLE), ('}', SYNTAX))

    def test_dict_variable(self):
        self._verify('&{my var}',
                     ('&{', SYNTAX), ('my var', VARIABLE), ('}', SYNTAX))

    def test_environment_variable(self):
        self._verify('%{VAR_NAME}',
                     ('%{', SYNTAX), ('VAR_NAME', VARIABLE), ('}', SYNTAX))

    def test_normal_texst_and_variable(self):
        self._verify("can haz @{var}?!??!!",
                     ('can haz ', ARGUMENT),
                     ('@{', SYNTAX), ('var', VARIABLE), ('}', SYNTAX),
                     ('?!??!!', ARGUMENT))

    def test_string_with_multiple_variables(self):
        self._verify("${var} + ${bar}@{x}",
                     ('${', SYNTAX), ('var', VARIABLE), ('}', SYNTAX),
                     (' + ', ARGUMENT),
                     ('${', SYNTAX), ('bar', VARIABLE), ('}', SYNTAX),
                     ('@{', SYNTAX), ('x', VARIABLE), ('}', SYNTAX))

    def test_escaping(self):
        self._verify('\\${not var}', ('\\${not var}', ARGUMENT))
        self._verify('-\\${a}-\\${b}-', ('-\\${a}-\\${b}-', ARGUMENT))

    def test_internal(self):
        self._verify('${var${inside}}',
                     ('${', SYNTAX), ('var', VARIABLE), ('${', SYNTAX),
                     ('inside', VARIABLE), ('}', SYNTAX), ('}', SYNTAX))
        self._verify('@{%{var${not}} end',
                     ('@{', SYNTAX), ('%{', SYNTAX), ('var${not', VARIABLE),
                     ('}', SYNTAX), ('}', SYNTAX), (' end', ARGUMENT))

    def test_var_item(self):
        self._verify('${var}[0] has item',
                     ('${', SYNTAX), ('var', VARIABLE), ('}', SYNTAX),
                     ('[', SYNTAX), ('0', VARIABLE), (']', SYNTAX),
                     (' has item', ARGUMENT))

    def test_var_item_with_variable(self):
        self._verify('${var}[${item}] has item with var',
                     ('${', SYNTAX), ('var', VARIABLE), ('}', SYNTAX),
                     ('[', SYNTAX),
                     ('${', SYNTAX), ('item', VARIABLE), ('}', SYNTAX),
                     (']', SYNTAX),
                     (' has item with var', ARGUMENT))

    def test_var_items(self):
        self._verify('${var}[0][key][ ${x}1 ] has items',
                     ('${', SYNTAX), ('var', VARIABLE), ('}', SYNTAX),
                     ('[', SYNTAX), ('0', VARIABLE), (']', SYNTAX),
                     ('[', SYNTAX), ('key', VARIABLE), (']', SYNTAX),
                     ('[', SYNTAX), (' ', VARIABLE),
                     ('${', SYNTAX), ('x', VARIABLE), ('}', SYNTAX),
                     ('1 ', VARIABLE), (']', SYNTAX),
                     (' has items', ARGUMENT))

    def test_list_var_item(self):
        self._verify('@{var}[ 0] is special',
                     ('@{', SYNTAX), ('var', VARIABLE), ('}', SYNTAX),
                     ('[', SYNTAX), (' 0', VARIABLE), (']', SYNTAX),
                     (' is special', ARGUMENT))

    def test_list_var_index_with_variable(self):
        self._verify('@{var}[${i}] end',
                     ('@{', SYNTAX), ('var', VARIABLE), ('}', SYNTAX),
                     ('[', SYNTAX), ('${', SYNTAX), ('i', VARIABLE),
                     ('}', SYNTAX), (']', SYNTAX), (' end', ARGUMENT))

    def test_dict_var_index(self):
        self._verify('&{var}[ 0] is special',
                     ('&{', SYNTAX), ('var', VARIABLE), ('}', SYNTAX),
                     ('[', SYNTAX), (' 0', VARIABLE), (']', SYNTAX),
                     (' is special', ARGUMENT))

    def test_dict_var_index_with_variable(self):
        self._verify('&{var}[${i}] end',
                     ('&{', SYNTAX), ('var', VARIABLE), ('}', SYNTAX),
                     ('[', SYNTAX), ('${', SYNTAX), ('i', VARIABLE),
                     ('}', SYNTAX), (']', SYNTAX), (' end', ARGUMENT))

    def test_var_items_escaped(self):
        for prefix in '$@&':
            self._verify(prefix + '{var}\\[0] has no items',
                         (prefix + '{', SYNTAX), ('var', VARIABLE), ('}', SYNTAX),
                         ('\\[0] has no items', ARGUMENT))


class TestForLoopTokenizer(unittest.TestCase):

    def _verify(self, loop, *expected):
        loop = '\n'.join('    '+ line for line in loop.splitlines())
        test = '*** Test Cases ***\nLooping\n' + loop
        actual = list(RobotFrameworkLexer().get_tokens(test))
        expected = [(HEADING, '*** Test Cases ***'),
                    (SYNTAX, '\n'),
                    (TC_KW_NAME, 'Looping'),
                    (SYNTAX, '\n'),
                    (SYNTAX, '    ')] + list(expected) + [(SYNTAX, '\n')]
        self.assertEqual(len(actual), len(expected))
        for act, exp in zip(actual, expected):
            self.assertEqual(act, exp)

    def _tokenize(self, string):
        tokenizer = ForLoop()
        for item in string.split():
            yield tokenizer.tokenize(item)

    def test_in(self):
        SEP = (SYNTAX, '    ')
        self._verify('FOR    ${x}    IN    foo    bar',
                     (SYNTAX, 'FOR'), SEP,
                     (SYNTAX, '${'), (VARIABLE, 'x'), (SYNTAX, '}'), SEP,
                     (SYNTAX, 'IN'), SEP,
                     (ARGUMENT, 'foo'), SEP, (ARGUMENT, 'bar'))

    def test_in_range(self):
        SEP = (SYNTAX, '    ')
        self._verify('FOR    ${index}    IN RANGE    1    ${10}',
                     (SYNTAX, 'FOR'), SEP,
                     (SYNTAX, '${'), (VARIABLE, 'index'), (SYNTAX, '}'), SEP,
                     (SYNTAX, 'IN RANGE'), SEP,
                     (ARGUMENT, '1'), SEP,
                     (SYNTAX, '${'), (VARIABLE, '10'), (SYNTAX, '}'))

    def test_in_enumerate(self):
        SEP = (SYNTAX, '    ')
        self._verify('FOR    ${index}    ${item}    IN ENUMERATE    foo    bar',
                     (SYNTAX, 'FOR'), SEP,
                     (SYNTAX, '${'), (VARIABLE, 'index'), (SYNTAX, '}'), SEP,
                     (SYNTAX, '${'), (VARIABLE, 'item'), (SYNTAX, '}'), SEP,
                     (SYNTAX, 'IN ENUMERATE'), SEP,
                     (ARGUMENT, 'foo'), SEP, (ARGUMENT, 'bar'))

    def test_in_zip(self):
        SEP = (SYNTAX, '    ')
        self._verify('FOR    ${x}    ${y}    IN ZIP    ${XXX}    ${YYY}',
                     (SYNTAX, 'FOR'), SEP,
                     (SYNTAX, '${'), (VARIABLE, 'x'), (SYNTAX, '}'), SEP,
                     (SYNTAX, '${'), (VARIABLE, 'y'), (SYNTAX, '}'), SEP,
                     (SYNTAX, 'IN ZIP'), SEP,
                     (SYNTAX, '${'), (VARIABLE, 'XXX'), (SYNTAX, '}'), SEP,
                     (SYNTAX, '${'), (VARIABLE, 'YYY'), (SYNTAX, '}'))

    def test_old_for(self):
        SEP = (SYNTAX, '    ')
        self._verify(': FOR    ${x}    IN    foo    bar',
                     (SYNTAX, ': FOR'), SEP,
                     (SYNTAX, '${'), (VARIABLE, 'x'), (SYNTAX, '}'), SEP,
                     (SYNTAX, 'IN'), SEP,
                     (ARGUMENT, 'foo'), SEP, (ARGUMENT, 'bar'))

    def test_case_sensitive(self):
        SEP = (SYNTAX, '    ')
        self._verify('FOR    ${x}    in    foo    bar',
                     (SYNTAX, 'FOR'), SEP,
                     (SYNTAX, '${'), (VARIABLE, 'x'), (SYNTAX, '}'), SEP,
                     (ERROR, 'in'), SEP,
                     (ERROR, 'foo'), SEP, (ERROR, 'bar'))

    def test_invalid_variable(self):
        SEP = (SYNTAX, '    ')
        self._verify('FOR    x    IN    foo    bar',
                     (SYNTAX, 'FOR'), SEP,
                     (ERROR, 'x'), SEP,
                     (SYNTAX, 'IN'), SEP,
                     (ARGUMENT, 'foo'), SEP, (ARGUMENT, 'bar'))

    def test_with_body_and_end(self):
        SEP = (SYNTAX, '    ')
        SEP2 = (SYNTAX, '        ')
        NEWLINE = (SYNTAX, '\n')
        self._verify('FOR    ${x}    IN    foo    bar\n    Log    ${x}\nEND',
                     (SYNTAX, 'FOR'), SEP,
                     (SYNTAX, '${'), (VARIABLE, 'x'), (SYNTAX, '}'), SEP,
                     (SYNTAX, 'IN'), SEP,
                     (ARGUMENT, 'foo'), SEP, (ARGUMENT, 'bar'), NEWLINE,
                     SEP2, (KEYWORD, 'Log'), SEP,
                     (SYNTAX, '${'), (VARIABLE, 'x'), (SYNTAX, '}'), NEWLINE,
                     SEP, (SYNTAX, 'END'))


class TestTrailingSpaces(unittest.TestCase):

    def _verify(self, text, *expected):
        actual = list(RobotFrameworkLexer().get_tokens_unprocessed(text))
        self.assertEqual(len(actual), len(expected))
        for act, exp in zip(actual, expected):
            self.assertEqual(act, exp)

    def test_space_separated(self):
        self._verify('*** Settings ***  \n'
                     'Library   NoTrail\n'
                     'Resource  trail   \n',
                     (0, HEADING, '*** Settings ***'),
                     (16, SEPARATOR, '  '),
                     (18, SEPARATOR, '\n'),
                     (19, SETTING, 'Library'),
                     (26, SEPARATOR, '   '),
                     (29, IMPORT, 'NoTrail'),
                     (36, SEPARATOR, '\n'),
                     (37, SETTING, 'Resource'),
                     (45, SEPARATOR, '  '),
                     (47, IMPORT, 'trail'),
                     (52, SEPARATOR, '   '),
                     (55, SEPARATOR, '\n'))

    def test_pipe_separated(self):
        self._verify('| *** Settings *** |  \n'
                     '| Library  | NoTrail |\n'
                     '| Resource | trail   |  \n',
                     (0, SEPARATOR, '| '),
                     (2, HEADING, '*** Settings ***'),
                     (18, SEPARATOR, ' |  '),
                     (22, SEPARATOR, '\n'),
                     (23, SEPARATOR, '| '),
                     (25, SETTING, 'Library'),
                     (32, SEPARATOR, '  | '),
                     (36, IMPORT, 'NoTrail'),
                     (43, SEPARATOR, ' |'),
                     (45, SEPARATOR, '\n'),
                     (46, SEPARATOR, '| '),
                     (48, SETTING, 'Resource'),
                     (56, SEPARATOR, ' | '),
                     (59, IMPORT, 'trail'),
                     (64, SEPARATOR, '   |  '),
                     (70, SEPARATOR, '\n'))


if __name__ == '__main__':
    unittest.main()
