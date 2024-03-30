# CS5421 Project

## Datalog-compiler

### Structure
```
├── requirements.txt (Contains the dependencies)
├── src (Contains the main code)
│   ├── backend (Contains the logic for the backend of the compiler)
│   │   ├── interpreter.py
│   │   └── sql_statement.py
│   ├── common (Contains the common items shared between the front end and the backend)
│   │   └── node_names.py
│   ├── datalog.txt (Some sample datalog queries can be found here. You can also pass in the commands from here)
│   ├── frontend (Contains the logic for the frontend of the compiler)
│   │   ├── lexer.py
│   │   ├── parser.out
│   │   ├── parser.py
│   │   └── parsetab.py
│   └── main.py
└── tests (Contains the unit test)
    ├── frontend
    │   └── test_lexer.py (Contains some unit tests for the lexer)
    └── test_main.py (Contains sample queries you can refer to)
```

### Running the application

Application can be run from the `datalog-compiler` using the following command:
```
python3 src/main.py
```

You can choose to run the queries as a
1. REPL
2. from the file (default from datalog.txt)

Select the options as you want

Also, sample queries that has been tested with can be found in datalog.txt and in the unittests test_main.py

### Dependencies:
Dependencies can be installed using the following command:
```
python3 -m pip install -r requirements.txt
```

### Unit tests:
Unit test can be run inside the `datalog-compiler` directory using the following command:
```
python3 -m unittest
```