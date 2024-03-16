import ply.lex as lex

tokens = (
    'IDENTIFIER',
    'VARIABLE',
    'STRING',
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
    'COMMENT'
)

def t_BOOLEAN(t):
    r'\btrue|false\b'
    t.value = t.value == 'true'
    return t

def t_STRING(t):
    r'"(?:[^\\]|\\.)*"'
    t.value = t.value[1:-1]
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
t_VARIABLE = r'[A-Z]\w*'
t_IDENTIFIER=r'[a-z][a-zA-Z0-9_-]*'

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
