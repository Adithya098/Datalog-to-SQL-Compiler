import sys,os
# Get the absolute path to the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the directory you want to add
module_dir = os.path.join(script_dir, 'datalog_compiler', 'src')

# Add the directory to sys.path
sys.path.append(module_dir)

from flask import Flask, request, jsonify
from flask_cors import CORS
from datalog_compiler.src.main import generate_sql_query_from_datalog_query, sql_connection, append_to_sql_file
# import datalog_compiler.src.main  as a
# import datalog_compiler.src.backend.interpreter as b
from datalog_compiler.src.backend.interpreter import Interpreter

from datetime import datetime
from decimal import Decimal

app = Flask(__name__)
CORS(app)
# Initialize the interpreter as a global variable
translate_interpreter = None
execute_interpreter = None
sql_handler = None


def initialize_translate_interpreter():
    global translate_interpreter
    if translate_interpreter is None:
        translate_interpreter = Interpreter()

def initialize_execute_interpreter():
    global execute_interpreter
    if execute_interpreter is None:
        execute_interpreter = Interpreter()


def initialize_sql_handler(output_file, db_database, db_username, db_password, db_port):
    global sql_handler
    if sql_handler is None:
        sql_handler = sql_connection(output_file, db_database, db_username, db_password, db_port)

def prettify_tuple_response(tuple_response):
    def prettify(response):
        if isinstance(response, datetime):
            return response.isoformat()
        if isinstance(response, Decimal):
            if Decimal(response) % 1 == 0:
                return str(int(response))
            return str(float(response))
        return str(response)
    return ", ".join([prettify(response) for response in tuple_response])

@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    text = data.get('text')
    return jsonify({'echo': text})

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    datalog_query = data.get('text')

    initialize_translate_interpreter()

    # interpreter = Interpreter()
    # generate_sql_query_from_datalog_query(datalog_query, interpreter)

    # return jsonify({'echo':  a.generate_sql_query_from_datalog_query(datalog_query, interpreter)})
    return jsonify({'translate':  generate_sql_query_from_datalog_query(datalog_query, translate_interpreter)})


@app.route('/execute_query', methods=['POST'])
def execute_query():
    data = request.get_json()
    datalog_query = data.get('text')
    db_username = data.get('username')
    db_password = data.get('password')
    db_port = data.get('port')
    db_database = data.get('database')
    output_file = "output.sql"
    initialize_execute_interpreter()
    initialize_sql_handler(output_file, db_database, db_username, db_password, db_port)

    def is_valid_statement(statement):
        return not statement == "---- Invalid statement"

    sql_queries = generate_sql_query_from_datalog_query(datalog_query, execute_interpreter)
    infos = []
    for sql_query in sql_queries:
        if not is_valid_statement(sql_query):
            infos.append("Not executed")
            continue
        info = sql_handler.execute_sql_query_from_frontend(sql_query)
        if not []:
            append_to_sql_file(sql_query, output_file)
        infos.extend(info)
    infos = [prettify_tuple_response(info) if type(info) is tuple else info for info in infos]
    return jsonify({'execute_query': infos, 'translate': sql_queries})


if __name__ == '__main__':
    app.run(debug=True, port=5002)



