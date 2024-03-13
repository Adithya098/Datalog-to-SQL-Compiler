import unittest
from src.frontend.lexer import lex
from src.frontend.token import Token
from parameterized import parameterized


class TestLexer(unittest.TestCase):

    @parameterized.expand([
        ["(", Token.LEFT_BRACKET,],
        [")", Token.RIGHT_BRACKET],
        ["[", Token.LEFT_SQUARE_BRACKET],
        ["]", Token.RIGHT_SQUARE_BRACKET]
    ])
    def test_individual_characters(self, arg, expected):
        res = lex(arg)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0], expected)
    
    @parameterized.expand([
        ["()", [Token.LEFT_BRACKET, Token.RIGHT_BRACKET]],
        ["[]", [Token.LEFT_SQUARE_BRACKET, Token.RIGHT_SQUARE_BRACKET]],
    ])
    def test_combinations_of_characters(self, arg, expected):
        res = lex(arg)
        self.assertEqual(len(res), len(expected))
        self.assertEqual(res, expected)

if __name__ == '__main__':
    unittest.main()