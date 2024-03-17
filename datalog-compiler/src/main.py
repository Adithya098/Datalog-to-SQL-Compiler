from frontend import parser
from backend.interpreter import Interpreter
import traceback
import os
import sys

def generate_sql_query_from_datalog_query(datalog_query, interpreter=Interpreter()):
    ast = parser.parse(datalog_query)
    sql_statements = interpreter.interpret(ast)
    for sql_statement in sql_statements:
        print(sql_statement)
    return sql_statements

def get_datalog_queries_from_file(file_path):
    with open(file_path, 'r') as content_file:
        datalog_queries = content_file.read()
    return datalog_queries

if __name__ == "__main__":
    choice_of_running = input('Would you like to run this as 1) REPL or 2) get query from dataset? Please input 1 or 2.')
    if choice_of_running == '1':
        isREPL = True
    elif choice_of_running == '2':
        isREPL = False
    else:
        print("Invalid input")
        sys.exit(1)
    interpreter = Interpreter()
    while True:
        try:
            if isREPL:
                datalog_query = input('What is the datalog query?\n')
                generate_sql_query_from_datalog_query(datalog_query, interpreter)
            else:
                file_path = input('What file do you want to read it from? Please provide the absolute path. Default: datalog.txt from current directory')
                if not file_path:
                    print(os.getcwd())
                    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "datalog.txt")
                datalog_queries = get_datalog_queries_from_file(file_path)
                generate_sql_query_from_datalog_query(datalog_queries)
                break
        except KeyboardInterrupt:
            print("Quitting")
            sys.exit(1)
        except Exception:
            traceback.print_exc()
            if not isREPL:
                sys.exit(1)
