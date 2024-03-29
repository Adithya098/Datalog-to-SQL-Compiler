import unittest
from src.frontend.lexer import get_tokens
from parameterized import parameterized


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
        ["/", "DIVISION", "/"]
    ])
    def test_individual_characters(self, arg, expected_token_type, expected_value):
        tokens = get_tokens(arg)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, expected_token_type)
        if expected_value is not None:
            self.assertEqual(tokens[0].value, expected_value)

if __name__ == '__main__':
    unittest.main()