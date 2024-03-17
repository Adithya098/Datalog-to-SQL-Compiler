import unittest
from src.main import generate_sql_query_from_datalog_query
from src.backend.sql_statement import *

class TestMain(unittest.TestCase):
    def test_basic_queries(self):
        datalog_queries = '''
        s(x, y).
        s(y, z).
        s(x, y)?
        s(x, Y)?
        s(X, y)?
        s(X, Y)?
        '''
        expected_translated_queries = [
            get_create_and_insert_statement('s', ['x', 'y'])[0],
            get_create_and_insert_statement('s', ['x', 'y'])[1],
            get_insert_statement('s', ['y', 'z'])[0],
            get_basic_query_statement('s', {0: 'x', 1: 'y'})[0],
            get_basic_query_statement('s', {0: 'x'})[0],
            get_basic_query_statement('s', {1: 'y'})[0],
            get_basic_query_statement('s', {})[0]
        ]
        actual_translated_queries = generate_sql_query_from_datalog_query(datalog_queries)
        for actual_translated_query, expected_translated_query in zip(actual_translated_queries, expected_translated_queries):
            self.assertEqual(actual_translated_query, expected_translated_query)

if __name__ == '__main__':
    unittest.main()