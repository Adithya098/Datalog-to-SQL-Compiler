import ply.lex as lex
from datetime import datetime

tokens = (
    'IDENTIFIER',
    'VARIABLE',
    'STRING',
    'DATETIME',
    'INTEGER',
    'BOOLEAN',
    'DECIMAL',
    'COMMA',
    'TILDE',
    'QUESTION_MARK',
    'LEFT_BRACKET',
    'RIGHT_BRACKET',
    "HEAD_AND_BODY_SEPARATOR",
    'NOT_EQUAL',
    'EQUAL',
    'COMMENT',
    'IGNORE',
    'LESS_THAN',
    'MORE_THAN',
    'LESS_THAN_OR_EQUAL_TO',
    'MORE_THAN_OR_EQUAL_TO',
    'NOT_EQUAL_ALT',
    'PLUS',
    'MINUS',
    'DIVISION',
    'MULTIPLY'
)

def t_BOOLEAN(t):
    r'\btrue|false\b'
    t.value = t.value == 'true'
    return t

def t_STRING(t):
    r'"(?:[^\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t

def t_DATETIME(t):
    r'^\d{4}(-\d\d(-\d\d((T|\s)\d\d:\d\d(:\d\d)?(\.\d+)?(([+-]\d\d:\d\d)|Z)?)?)?)?$'
    t.value = datetime.fromisoformat(t.value)
    return t

def t_INTEGER(t):
    r'-?(?:0|[1-9][0-9]*)'
    t.value = int(t.value)
    return t

t_DECIMAL = r'\.'
t_COMMA = r'\,'
t_TILDE = r'\~'
t_QUESTION_MARK = r'\?'
t_LEFT_BRACKET = r'\('
t_RIGHT_BRACKET = r'\)'
t_HEAD_AND_BODY_SEPARATOR = r'\:-'
t_NOT_EQUAL = r'\!='
t_EQUAL = r'\='
t_LESS_THAN = r'\<'
t_MORE_THAN = r'\>'
t_LESS_THAN_OR_EQUAL_TO = r'\<='
t_MORE_THAN_OR_EQUAL_TO = r'\>='
t_NOT_EQUAL_ALT = r'\<>'
t_VARIABLE = r'[A-Z]\w*'
t_IDENTIFIER=r'[a-z][a-zA-Z0-9_-]*'
t_IGNORE = r'\_'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVISION = r'\/'
t_MULTIPLY = r'\*'

t_ignore_COMMENT = r'\%.*'

t_ignore = ' \t\n'

def t_error(t):
    print("Error found while lexing: " + str(t))
    raise Exception("Lexing Error")

lexer = lex.lex()

def get_tokens(data):
    lexer.input(data)
    tokens = []
    while True:
        token = lexer.token()
        if not token:
            break
        tokens.append(token)
    return tokens
