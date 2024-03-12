from frontend import parser
from backend import interpreter

if __name__ == "__main__":
    parser.parse()
    interpreter.interpret()