import ply.yacc as yacc
from frontend.lexer import tokens

def p_program(p):
    '''
    program : statement program
            | statement
            | empty
    '''
    if len(p) == 3:
        p[0] = ('program', [p[1]] + p[2][1])
    elif len(p) == 2:
        p[0] = ('program', [p[1]])
    else:
        p[0] = ('program', [])

def p_empty(_):
    'empty :'
    pass

def p_statement(p):
    '''
    statement : assertion
              | retraction
              | query
              | requirement
    '''
    p[0] = ('statement', p[1])

def p_assertion(p):
    '''
    assertion : clause DECIMAL
    '''
    p[0] = ('assertion', p[1], p[2])

def p_retraction(p):
    '''
    retraction : clause TILDE
    '''
    p[0] = ('clause', p[1], p[2])

def p_query(p):
    '''
    query : literal QUESTION_MARK
    '''
    p[0] = ('query', p[1], p[2])

def p_requirement(p):
    '''
    requirement : LEFT_BRACKET IDENTIFIER RIGHT_BRACKET
    '''
    p[0] = ('requirement', p[1], p[2], p[3])

def p_clause(p):
    '''
    clause : literal HEAD_AND_BODY_SEPARATOR body
           | literal
    '''
    if len(p) == 4:
        p[0] = ('clause', p[1], p[2], p[3])
    else:
        p[0] = ('clasue', p[1])

def p_body(p):
    '''
    body : literal COMMA body
         | literal
    '''
    if len(p) == 4:
        p[0] = ('body', p[1], p[2], p[3])
    else:
        p[0] = ('body', p[1])

def p_literal(p):
    '''
    literal : predicate LEFT_BRACKET RIGHT_BRACKET
            | predicate LEFT_BRACKET terms RIGHT_BRACKET
            | predicate
            | term EQUAL term
            | term NOT_EQUAL term
    '''
    # Note: Not expressing <VARIABLE> :- <external-sym> ( <terms> ) as BNF doesn't
    # explicitly define external-sym
    if len(p) == 5:
        p[0] = ('literal', p[1], p[2], p[3], p[4])
    elif len(p) == 4:
        p[0] = ('literal', p[1], p[2], p[3])
    else:
        p[0] = ('literal', p[1])

def p_predicate(p):
    '''
    predicate : IDENTIFIER
              | STRING
    '''
    p[0] = ('predicate', p[1])

def p_terms(p):
    '''
    terms : term terms
          | term
    '''
    if len(p) == 3:
        p[0] = ('terms', [p[1]] + p[2][1])
    else:
        p[0] = ('terms', [p[1]])

def p_term(p):
    '''
    term : VARIABLE
         | constant
    '''
    p[0] = ('term', p[1])

def p_constant(p):
    '''
    constant : IDENTIFIER
             | STRING
             | INTEGER
             | BOOLEAN
    '''
    p[0] = ('constant', p[1])

def p_error(p):
    print("Error when parsing: " + str(p))
    raise Exception("Parsing Error")

def parse(datalog_query):
    parser = yacc.yacc()
    result = parser.parse(datalog_query)
    return result