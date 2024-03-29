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
app = Flask(__name__)
CORS(app)
# Initialize the interpreter as a global variable
interpreter = None
sql_handler = None


def initialize_interpreter():
    global interpreter
    if interpreter is None:
        interpreter = Interpreter()


def initialize_sql_handler(output_file, db_database, db_username, db_password, db_port):
    global sql_handler
    if sql_handler is None:
        sql_handler = sql_connection(output_file, db_database, db_username, db_password, db_port)


@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    text = data.get('text')
    return jsonify({'echo': text})

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    datalog_query = data.get('text')

    datalog_query = data.get('text')

    db_username = data.get('username')
    db_password = data.get('password')
    db_port = data.get('port')
    db_database = data.get('database')

    output_file = "output.sql"
    initialize_sql_handler(output_file, db_database, db_username, db_password, db_port)

    # interpreter = Interpreter()
    # generate_sql_query_from_datalog_query(datalog_query, interpreter)

    # return jsonify({'echo':  a.generate_sql_query_from_datalog_query(datalog_query, interpreter)})
    return jsonify({'translate':  generate_sql_query_from_datalog_query(datalog_query, interpreter)})


@app.route('/execute_query', methods=['POST'])
def execute_query():
    data = request.get_json()
    datalog_query = data.get('text')

    output_file = "output.sql"
    initialize_interpreter()

    sql_queries = generate_sql_query_from_datalog_query(datalog_query, interpreter)
    
    for sql_query in sql_queries:
        info = sql_handler.execute_sql_query_from_frontend(sql_query)
        if []:
            return jsonify({'execute_query': info})
        else:
            append_to_sql_file(sql_query, output_file)

    return jsonify({'execute_query': info})


if __name__ == '__main__':
    app.run(debug=True, port=5002)



