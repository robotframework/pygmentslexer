import unittest

from robotframeworklexer import *


class TestVariableFinder(unittest.TestCase):

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
                     ('${', VAR_DECO), ('variable', VAR_BASE), ('}', VAR_DECO))

    def test_list_variable(self):
        self._verify('@{my var}',
                     ('@{', VAR_DECO), ('my var', VAR_BASE), ('}', VAR_DECO))

    def test_normal_texst_and_variable(self):
        self._verify("can haz @{var}?!??!!",
                     ('can haz ', ARGUMENT),
                     ('@{', VAR_DECO), ('var', VAR_BASE), ('}', VAR_DECO),
                     ('?!??!!', ARGUMENT))

    def test_string_with_multiple_variables(self):
        self._verify("${var} + ${bar}&@{x}",
                     ('${', VAR_DECO), ('var', VAR_BASE), ('}', VAR_DECO),
                     (' + ', ARGUMENT),
                     ('${', VAR_DECO), ('bar', VAR_BASE), ('}', VAR_DECO),
                     ('&', ARGUMENT),
                     ('@{', VAR_DECO), ('x', VAR_BASE), ('}', VAR_DECO))

    def test_escaping(self):
        self._verify('\\${not var}', ('\\${not var}', ARGUMENT))
        self._verify('-\\${a}-\\${b}-', ('-\\${a}-\\${b}-', ARGUMENT))

    def test_internal(self):
        self._verify('${var${inside}}',
                     ('${', VAR_DECO), ('var', VAR_BASE), ('${', VAR_DECO),
                     ('inside', VAR_BASE), ('}', VAR_DECO), ('}', VAR_DECO))
        self._verify('@{${var${not}}',
                     ('@{', VAR_DECO), ('${', VAR_DECO), ('var${not', VAR_BASE),
                     ('}', VAR_DECO), ('}', VAR_DECO))

    def test_list_var_index(self):
        self._verify('${var}[0] is not special',
                     ('${', VAR_DECO), ('var', VAR_BASE), ('}', VAR_DECO),
                     ('[0] is not special', ARGUMENT))
        self._verify('@{var}[ 0] is special',
                     ('@{', VAR_DECO), ('var', VAR_BASE), ('}', VAR_DECO),
                     ('[', VAR_DECO), (' 0', VAR_BASE), (']', VAR_DECO),
                     (' is special', ARGUMENT))

    def test_list_var_index_with_variable(self):
        self._verify('@{var}[${i}]',
                     ('@{', VAR_DECO), ('var', VAR_BASE), ('}', VAR_DECO),
                     ('[', VAR_DECO), ('${', VAR_DECO), ('i', VAR_BASE),
                     ('}', VAR_DECO), (']', VAR_DECO))
