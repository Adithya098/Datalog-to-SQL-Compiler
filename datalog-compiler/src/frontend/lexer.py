from src.frontend.token import Token

def lex(datalog_query_string):
    def advance_start_and_current():
        nonlocal start
        nonlocal current
        start += 1
        current += 1

    start = 0
    current = 0
    tokens = []

    for ch in datalog_query_string:
        match ch:
            case "(":
                tokens.append(Token.LEFT_BRACKET)
                advance_start_and_current()
            case ")":
                tokens.append(Token.RIGHT_BRACKET)
                advance_start_and_current()
            case "[":
                tokens.append(Token.LEFT_SQUARE_BRACKET)
                advance_start_and_current()
            case "]":
                tokens.append(Token.RIGHT_SQUARE_BRACKET)
                advance_start_and_current()

    return tokens
            
        
        