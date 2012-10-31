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

    def test_string_without_variable(self):
        self._verify('text', ('text', ARGUMENT))

    def test_string_with_basic_variable(self):
        self._verify("${variable}",
                     ('${', VAR_DECO),
                     ('variable', VAR_BASE),
                     ('}', VAR_DECO))

    def test_string_with_two_variables(self):
        self._verify("${var} test ${bar}",
                    ('${', VAR_DECO),
                    ('var', VAR_BASE),
                    ('}', VAR_DECO),
                    (' test ', ARGUMENT),
                    ('${', VAR_DECO),
                    ('bar', VAR_BASE),
                    ('}', VAR_DECO))
