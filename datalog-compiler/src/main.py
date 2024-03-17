from frontend import parser
from backend.interpreter import Interpreter
import traceback

def generate_sql_query_from_datalog_query(datalog_query, interpreter=Interpreter()):
    ast = parser.parse(datalog_query)
    sql_statements = interpreter.interpret(ast)
    for sql_statement in sql_statements:
        print(sql_statement)

if __name__ == "__main__":
    interpreter = Interpreter()
    while True:
        try:
            datalog_query = input('What is the datalog query?\n')
            res = generate_sql_query_from_datalog_query(datalog_query, interpreter)
        except KeyboardInterrupt:
            print("Quitting")
            break
        except Exception:
            traceback.print_exc()
