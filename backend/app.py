from flask import Flask, request, jsonify
from flask_cors import CORS
# from datalog_compiler.src.main import generate_sql_query_from_datalog_query
# from datalog_compiler.src.backend.interpreter import Interpreter
from datalog_compiler import Interpreter
app = Flask(__name__)
CORS(app)

@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    text = data.get('text')
    return jsonify({'echo': text})

@app.route('/translate', methods=['POST'])
def echo():
    data = request.get_json()
    datalog_query = data.get('text')

    interpreter = Interpreter()
    # generate_sql_query_from_datalog_query(datalog_query, interpreter)

    return jsonify({'echo':  generate_sql_query_from_datalog_query(datalog_query, interpreter)})




if __name__ == '__main__':
    app.run(debug=True, port=5002)

