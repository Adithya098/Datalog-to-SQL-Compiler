import sys,os
# Get the absolute path to the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the directory you want to add
module_dir = os.path.join(script_dir, 'datalog_compiler', 'src')

# Add the directory to sys.path
sys.path.append(module_dir)

from flask import Flask, request, jsonify
from flask_cors import CORS
from datalog_compiler.src.main import generate_sql_query_from_datalog_query
# import datalog_compiler.src.main  as a
# import datalog_compiler.src.backend.interpreter as b
from datalog_compiler.src.backend.interpreter import Interpreter
app = Flask(__name__)
CORS(app)

@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    text = data.get('text')
    return jsonify({'echo': text})

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    datalog_query = data.get('text')

    interpreter = Interpreter()
    # generate_sql_query_from_datalog_query(datalog_query, interpreter)

    # return jsonify({'echo':  a.generate_sql_query_from_datalog_query(datalog_query, interpreter)})
    return jsonify({'translate':  generate_sql_query_from_datalog_query(datalog_query, interpreter)})




if __name__ == '__main__':
    app.run(debug=True, port=5002)


