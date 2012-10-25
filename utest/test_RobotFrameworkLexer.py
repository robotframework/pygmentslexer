from unittest import TestCase
from robotframeworklexer import COMMENT, RobotFrameworkLexer, HEADING


class TestComment(TestCase):

    def setUp(self):
        self.lexer = RobotFrameworkLexer()

    def test_empty_comment_row(self):
        tokens = self.lexer.get_tokens('#comment')
        self.assertIn((COMMENT, '#comment\n'), tokens)

    def test_line_ending_with_comment(self):
        tokens = self.lexer.get_tokens('*** Test cases *** #comment with text\n')
        self.assertIn((COMMENT, '#comment with text\n'), tokens)

    def test_comment_can_be_inside_settings(self):
        tokens = self.lexer.get_tokens('*** Settings ***\n'
                                       '#comment\n'
                                       'Library    OperatingSystem')
        self.assertIn((COMMENT, '#comment\n'), tokens)

    def test_comment_can_be_inside_tests(self):
        tokens = self.lexer.get_tokens('*** Test cases ***\n'
                                       '#comment1\n'
                                       'Test name\n'
                                       '#comment2\n'
                                       '    #comment3\n'
                                       '    Keyword\n')
        self.assertIn((COMMENT, '#comment1\n'), tokens)
        self.assertIn((COMMENT, '#comment2\n'), tokens)
        self.assertIn((COMMENT, '#comment3\n'), tokens)


class TestSettings(TestCase):

    def setUp(self):
        self.lexer = RobotFrameworkLexer()
        self.settings_text = '*** Settings ***\n' \
                             'Library    OperatingSystem\n' \
                             'Force Tags    foo    bar    zig\n' \
                             'Resource    resources.txt\n'

    def test_settings_should_have_heading(self):
        tokens = self.lexer.get_tokens(self.settings_text)
        self.assertIn((HEADING, '*** Settings ***\n'), tokens)
