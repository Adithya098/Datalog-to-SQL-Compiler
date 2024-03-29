import unittest
from src.frontend.lexer import get_tokens
from parameterized import parameterized
from datetime import datetime


class TestLexer(unittest.TestCase):
    @parameterized.expand([
        ["true", "BOOLEAN", 1, True],
        ["false", "BOOLEAN", 1, False],
        [".", "DECIMAL", 1, "."],
        [",", "COMMA", 1, ","],
        ["~", "TILDE", 1, "~"],
        ["?", "QUESTION_MARK", 1, "?"],
        ["(", "LEFT_BRACKET", 1, "("],
        [")", "RIGHT_BRACKET", 1, ")"],
        [":-", "HEAD_AND_BODY_SEPARATOR", 1, ":-"],
        ["!=", "NOT_EQUAL", 1, "!="],
        ["=", "EQUAL", 1, "="],
        ["\"abcd\"", "STRING", 1, "abcd"],
        ["N1", "VARIABLE", 1, "N1"],
        ["false", "BOOLEAN", 1, False],
        ["123", "INTEGER", 1, 123],
        ["abcd", "IDENTIFIER", 1, "abcd"],
        ["<", "LESS_THAN", 1, "<"],
        [">", "MORE_THAN", 1, ">"],
        ["<=", "LESS_THAN_OR_EQUAL_TO", 1, "<="],
        [">=", "MORE_THAN_OR_EQUAL_TO", 1, ">="],
        ["<>", "NOT_EQUAL_ALT", 1, "<>"],
        ["+", "PLUS", 1, "+"],
        ["-", "MINUS", 1, "-"],
        ["*", "MULTIPLY", 1, "*"],
        ["/", "DIVISION", 1, "/"],
        ["2019-05-19", "DATETIME", 1, datetime.fromisoformat("2019-05-19")],
        ["2019-05-19 18:39:22", "DATETIME", 1, datetime.fromisoformat("2019-05-19 18:39:22")],
        ["2019-05-19T23:39:22", "DATETIME", 1, datetime.fromisoformat("2019-05-19T23:39:22")],
        ["2019-05-19T00:39:22Z", "DATETIME", 1, datetime.fromisoformat("2019-05-19T00:39:22Z")],
        ["2017-01-01 23:12:23+08:00", "DATETIME", 1, datetime.fromisoformat("2017-01-01 23:12:23+08:00")],
        ["NOW()", "FUNCTION", 3, "NOW"],
        ["FACTORIAL(17)", "FUNCTION", 4, "FACTORIAL"]
    ])
    def test_individual_characters(self, arg, expected_token_type, expected_length, expected_value):
        tokens = get_tokens(arg)
        self.assertEqual(len(tokens), expected_length)
        self.assertEqual(tokens[0].type, expected_token_type)
        if expected_value is not None:
            self.assertEqual(tokens[0].value, expected_value)

if __name__ == '__main__':
    unittest.main()