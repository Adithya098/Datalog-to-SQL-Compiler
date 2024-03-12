from frontend import parser
from backend import interpreter

if __name__ == "__main__":
    while True:
        datalog_query = input('What is the datalog query?\n')
        ast = parser.parse(datalog_query)
        sql = interpreter.interpret(ast)