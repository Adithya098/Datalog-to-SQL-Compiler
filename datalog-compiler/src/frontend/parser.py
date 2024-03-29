import ply.yacc as yacc
from frontend.lexer import tokens
from common.node_names import *

def p_program(p):
    '''
    program : statement program
            | statement
            | empty
    '''
    if len(p) == 3:
        p[0] = (PROGRAM_NODE, [p[1]] + p[2][1])
    elif len(p) == 2:
        p[0] = (PROGRAM_NODE, [p[1]])
    else:
        p[0] = (PROGRAM_NODE, [])

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
    p[0] = (STATEMENT_NODE, p[1])

def p_assertion(p):
    '''
    assertion : clause DECIMAL
    '''
    p[0] = (ASSERTION_NODE, p[1])

def p_retraction(p):
    '''
    retraction : clause TILDE
    '''
    p[0] = (RETRACTION_NODE, p[1])

def p_query(p):
    '''
    query : literal QUESTION_MARK
    '''
    p[0] = (QUERY_NODE, p[1])

def p_requirement(p):
    '''
    requirement : LEFT_BRACKET IDENTIFIER RIGHT_BRACKET DECIMAL
    '''
    p[0] = (REQUIREMENT_NODE, p[2])

def p_clause(p):
    '''
    clause : literal HEAD_AND_BODY_SEPARATOR body
           | literal
    '''
    if len(p) == 4:
        p[0] = (CLAUSE_NODE, p[2], p[1], p[3])
    else:
        p[0] = (CLAUSE_NODE, p[1])

def p_body(p):
    '''
    body : literal COMMA body
         | literal
    '''
    if len(p) == 4:
        p[0] = (BODY_NODE, [p[1]] + p[3][1])
    else:
        p[0] = (BODY_NODE, [p[1]])

def p_literal(p):
    '''
    literal : predicate LEFT_BRACKET RIGHT_BRACKET
            | predicate LEFT_BRACKET terms RIGHT_BRACKET
            | predicate
            | comparison
            | VARIABLE HEAD_AND_BODY_SEPARATOR IDENTIFIER LEFT_BRACKET terms RIGHT_BRACKET
    '''
    if len(p) == 6:
        p[0] = (LITERAL_NODE, p[1], p[2], p[3], p[4], p[5])
    elif len(p) == 5:
        p[0] = (LITERAL_NODE, p[1], p[2], p[3], p[4])
    elif len(p) == 4:
        p[0] = (LITERAL_NODE, p[1], p[2], p[3])
    else:
        p[0] = (LITERAL_NODE, p[1])

def p_predicate(p):
    '''
    predicate : IDENTIFIER
              | STRING
    '''
    p[0] = (PREDICATE_NODE, p[1])

def p_terms(p):
    '''
    terms : term COMMA terms
          | term
    '''
    if len(p) == 4:
        p[0] = (TERMS_NODE, [p[1]] + p[3][1])
    else:
        p[0] = (TERMS_NODE, [p[1]])

def p_term(p):
    '''
    term : VARIABLE
         | constant
         | IGNORE
    '''
    p[0] = (TERM_NODE, p[1])

def p_constant(p):
    '''
    constant : IDENTIFIER
             | STRING
             | INTEGER
             | BOOLEAN
    '''
    p[0] = (CONSTANT_NODE, p[1])

def p_comparison(p):
    '''
    comparison : comparisonterm EQUAL comparisonterm
               | comparisonterm NOT_EQUAL comparisonterm
               | comparisonterm LESS_THAN comparisonterm
               | comparisonterm MORE_THAN comparisonterm
               | comparisonterm LESS_THAN_OR_EQUAL_TO comparisonterm
               | comparisonterm MORE_THAN_OR_EQUAL_TO comparisonterm
               | comparisonterm NOT_EQUAL_ALT comparisonterm
    '''
    p[0] = (COMPARISON_NODE, p[1], p[2], p[3])

def p_comparisonterm(p):
    '''
    comparisonterm : term
    '''
    p[0] = (COMPARISON_TERM_NODE, p[1])

def p_error(p):
    print("Error when parsing: " + str(p))
    raise Exception("Parsing Error")

def parse(datalog_query):
    parser = yacc.yacc()
    result = parser.parse(datalog_query)
    return result