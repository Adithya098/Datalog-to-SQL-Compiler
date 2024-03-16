from frontend import parser
from backend import interpreter

def generate_sql_query_from_datalog_query(datalog_query):
    ast = parser.parse(datalog_query)
    print(ast)
    sql = interpreter.interpret(ast)
    print(sql)

if __name__ == "__main__":
    while True:
        try:
            datalog_query = input('What is the datalog query?\n')
            res = generate_sql_query_from_datalog_query(datalog_query)
        except KeyboardInterrupt:
            print("Quitting")
            break
        except Exception as e:
            print(e)
