import unittest
from src.frontend.lexer import get_tokens
from parameterized import parameterized
from datetime import datetime


class TestLexer(unittest.TestCase):
    @parameterized.expand([
        ["true", "BOOLEAN", True],
        ["false", "BOOLEAN", False],
        [".", "DECIMAL", "."],
        [",", "COMMA", ","],
        ["~", "TILDE", "~"],
        ["?", "QUESTION_MARK", "?"],
        ["(", "LEFT_BRACKET", "("],
        [")", "RIGHT_BRACKET", ")"],
        [":-", "HEAD_AND_BODY_SEPARATOR", ":-"],
        ["!=", "NOT_EQUAL", "!="],
        ["=", "EQUAL", "="],
        ["\"abcd\"", "STRING", "abcd"],
        ["N1", "VARIABLE", "N1"],
        ["false", "BOOLEAN", False],
        ["123", "INTEGER", 123],
        ["abcd", "IDENTIFIER", "abcd"],
        ["<", "LESS_THAN", "<"],
        [">", "MORE_THAN", ">"],
        ["<=", "LESS_THAN_OR_EQUAL_TO", "<="],
        [">=", "MORE_THAN_OR_EQUAL_TO", ">="],
        ["<>", "NOT_EQUAL_ALT", "<>"],
        ["+", "PLUS", "+"],
        ["-", "MINUS", "-"],
        ["*", "MULTIPLY", "*"],
        ["/", "DIVISION", "/"],
        ["2019-05-19", "DATETIME", datetime.fromisoformat("2019-05-19")],
        ["2019-05-19 18:39:22", "DATETIME", datetime.fromisoformat("2019-05-19 18:39:22")],
        ["2019-05-19T23:39:22", "DATETIME", datetime.fromisoformat("2019-05-19T23:39:22")],
        ["2019-05-19T00:39:22Z", "DATETIME", datetime.fromisoformat("2019-05-19T00:39:22Z")]
    ])
    def test_individual_characters(self, arg, expected_token_type, expected_value):
        tokens = get_tokens(arg)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, expected_token_type)
        if expected_value is not None:
            self.assertEqual(tokens[0].value, expected_value)

if __name__ == '__main__':
    unittest.main()