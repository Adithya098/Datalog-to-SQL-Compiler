from frontend import parser
from backend import interpreter

def generate_sql_query_from_datalog_query(datalog_query):
    ast = parser.parse(datalog_query)
    sql = interpreter.interpret(ast)
    print(sql)

if __name__ == "__main__":
    while True:
        datalog_query = input('What is the datalog query?\n')
        generate_sql_query_from_datalog_query(datalog_query)
