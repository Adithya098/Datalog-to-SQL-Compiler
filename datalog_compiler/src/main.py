import sys
from frontend import parser
from backend.interpreter import Interpreter
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import psycopg2
import os
import sys
import traceback
from sql_handler import SQLHandler

class SQLFileHandler(FileSystemEventHandler):
    def __init__(self, sql_handler, file_path):
        self.sql_handler = sql_handler
        self.file_path = file_path

    def on_modified(self, event):
        if event.src_path == self.file_path:
            print("SQL file modified. Reloading...")
            self.sql_handler.reload_sql_file(self.file_path)

def sql_connection(output_file, database="datalog_to_sql_db", username="postgres", pwd="", port_id=5432):
    # database = "datalog_compiler"
    # username = "postgres"
    # pwd = "postgres"
    # port_id = 5432

    try:
        conn = psycopg2.connect(dbname=database, user=username, password=pwd, port=port_id)
    except psycopg2.Error as e:
        print("Unable to connect to the database:", e)
        sys.exit(1)

    sql_handler = SQLHandler(conn)
    sql_handler.drop_all_objects()

    file_handler = SQLFileHandler(sql_handler, output_file)
    observer = Observer()
    observer.schedule(file_handler, os.path.dirname(os.path.abspath(output_file)), recursive=False)
    observer.start()

    return sql_handler


def generate_sql_query_from_datalog_query(datalog_query, interpreter=None):
    # print (sys.path)
    if not interpreter:
        interpreter = Interpreter()
    ast = parser.parse(datalog_query)
    sql_statements = interpreter.interpret(ast)
    for sql_statement in sql_statements:
        print(sql_statement)
    return sql_statements

def get_datalog_queries_from_file(file_path):
    with open(file_path, 'r') as content_file:
        datalog_queries = content_file.read()
    return datalog_queries

def append_to_sql_file(sql_query, output_file):
    with open(output_file, "a") as f:  
        f.write(sql_query + "\n\n")

if __name__ == "__main__":
    choice_of_running = input('Would you like to run this as 1) REPL or 2) get query from dataset? Please input 1 or 2.')
    if choice_of_running == '1':
        isREPL = True
    elif choice_of_running == '2':
        isREPL = False
    else:
        print("Invalid input")
        sys.exit(1)

    output_file = "output_queries.sql"  
    
    with open(output_file, "w") as f:  
        f.write("")  

    interpreter = Interpreter()

    # sql_handler = sql_connection(output_file)
    # database = "datalog_compiler"
    # username = "postgres"
    # pwd = "postgres"
    # port_id = 5432

    # try:
    #     conn = psycopg2.connect(dbname=database, user=username, password=pwd, port=port_id)
    # except psycopg2.Error as e:
    #     print("Unable to connect to the database:", e)
    #     sys.exit(1)

    # sql_handler = SQLHandler(conn)
    # sql_handler.drop_all_objects()

    # file_handler = SQLFileHandler(sql_handler, output_file)
    # observer = Observer()
    # observer.schedule(file_handler, os.path.dirname(os.path.abspath(output_file)), recursive=False)
    # observer.start()

    while True:
        try:
            if isREPL:
                datalog_query = input('What is the datalog query?\n')
                sql_queries = generate_sql_query_from_datalog_query(datalog_query, interpreter)
                for sql_query in sql_queries:
                    sql_handler.execute_sql_query(sql_query)
                    append_to_sql_file(sql_query, output_file)
            else:
                file_path = input('What file do you want to read it from? Please provide the absolute path. Default: datalog.txt from current directory')
                if not file_path:
                    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "datalog.txt")
                datalog_queries = get_datalog_queries_from_file(file_path)
                generate_sql_query_from_datalog_query(datalog_queries)
        except KeyboardInterrupt:
            print("Quitting")
            sys.exit(1)
        except Exception:
            traceback.print_exc()
            if not isREPL:
                sys.exit(1)

    observer.stop()
    observer.join()
    conn.close()