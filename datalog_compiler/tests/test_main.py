import unittest
from src.main import generate_sql_query_from_datalog_query
from src.backend.sql_statement_generator import *

class TestMain(unittest.TestCase):
    def test_basic_queries(self):
        datalog_queries = '''
        s(x, y).
        s(y, z).
        s(x, y)?
        s(x, Y)?
        s(X, y)?
        s(X, Y)?
        x(1, x).
        '''
        expected_translated_queries = [
            "CREATE TABLE s (z0 TEXT NOT NULL, z1 TEXT NOT NULL, PRIMARY KEY (z0, z1));",
            "INSERT INTO s VALUES ('x', 'y');",
            "INSERT INTO s VALUES ('y', 'z');",
            "SELECT * FROM s WHERE z0='x' AND z1='y';",
            "SELECT * FROM s WHERE z0='x';",
            "SELECT * FROM s WHERE z1='y';",
            "SELECT * FROM s;",
            "CREATE TABLE x (z0 INT NOT NULL, z1 TEXT NOT NULL, PRIMARY KEY (z0, z1));",
            "INSERT INTO x VALUES (1, 'x');"
        ]
        actual_translated_queries = generate_sql_query_from_datalog_query(datalog_queries)
        for actual_translated_query, expected_translated_query in zip(actual_translated_queries, expected_translated_queries):
            self.assertEqual(actual_translated_query, expected_translated_query)
    
    def test_basic_view(self):
        datalog_queries = '''
        s(x, y).
        s(y, z).
        t(X, Y) :- s(X, Y).
        t(X, Y)?
        u(X, Y) :- s(Y, X).
        u(X, Y)?
        v(X, Y) :- t(X, Z), u(Z, Y).
        v(X, Y)?
        w(X) :- s(X, Y).
        w(X)?
        '''
        expected_translated_queries = [
            "CREATE TABLE s (z0 TEXT NOT NULL, z1 TEXT NOT NULL, PRIMARY KEY (z0, z1));",
            "INSERT INTO s VALUES ('x', 'y');",
            "INSERT INTO s VALUES ('y', 'z');",
            "CREATE VIEW t AS (SELECT s.z0, s.z1 FROM s);",
            "SELECT * FROM t;",
            "CREATE VIEW u AS (SELECT s.z1, s.z0 FROM s);",
            "SELECT * FROM u;",
            "CREATE VIEW v AS (SELECT t.z0, u.z1 FROM t, u WHERE t.z1=u.z0);",
            "SELECT * FROM v;",
            "CREATE VIEW w AS (SELECT s.z0 FROM s);",
            "SELECT * FROM w;"
        ]
        actual_translated_queries = generate_sql_query_from_datalog_query(datalog_queries)
        for actual_translated_query, expected_translated_query in zip(actual_translated_queries, expected_translated_queries):
            self.assertEqual(actual_translated_query, expected_translated_query)
    
    def test_recursive_query(self):
        datalog_queries = '''
        link(a, b).
        link(b, c).
        link(c, c).
        link(c, d).
        reachable(X, Y) :- link(X, Y).
        reachable(X, Y) :- link(X, Z), reachable(Z, Y).
        reachable(X, Y)?
        '''
        expected_translated_queries = [
            "CREATE TABLE link (z0 TEXT NOT NULL, z1 TEXT NOT NULL, PRIMARY KEY (z0, z1));",
            "INSERT INTO link VALUES ('a', 'b');",
            "INSERT INTO link VALUES ('b', 'c');",
            "INSERT INTO link VALUES ('c', 'c');",
            "INSERT INTO link VALUES ('c', 'd');",
            "CREATE VIEW reachable AS WITH RECURSIVE reachable (z0, z1) AS ((SELECT link.z0, link.z1 FROM link) UNION DISTINCT (SELECT link.z0, reachable.z1 FROM link, reachable WHERE link.z1=reachable.z0)) SELECT * FROM reachable;",
            "SELECT * FROM reachable;"
        ]
        actual_translated_queries = generate_sql_query_from_datalog_query(datalog_queries)
        for actual_translated_query, expected_translated_query in zip(actual_translated_queries, expected_translated_queries):
            self.assertEqual(actual_translated_query, expected_translated_query)

    def test_ignore_query(self):
        datalog_queries = '''
        s(x, y).
        s(y, z).
        t(X) :- s(X, _).
        t(X)?
        y(X) :- s(_, X), t(X).
        y(X)?
        '''
        expected_translated_queries = [
            "CREATE TABLE s (z0 TEXT NOT NULL, z1 TEXT NOT NULL, PRIMARY KEY (z0, z1));",
            "INSERT INTO s VALUES ('x', 'y');",
            "INSERT INTO s VALUES ('y', 'z');",
            "CREATE VIEW t AS (SELECT s.z0 FROM s);",
            "SELECT * FROM t;",
            "CREATE VIEW y AS (SELECT s.z1 FROM s, t WHERE s.z1=t.z0);",
            "SELECT * FROM y;"
        ]
        actual_translated_queries = generate_sql_query_from_datalog_query(datalog_queries)
        for actual_translated_query, expected_translated_query in zip(actual_translated_queries, expected_translated_queries):
            self.assertEqual(actual_translated_query, expected_translated_query)

    def test_basic_comparison_query(self):
        datalog_queries = '''
        s(x, 1).
        s(y, 2).
        t(Y) :- s(_, Y), Y > 1.
        t(Y)?
        u(X, Y) :- s(X, Y), X = "y", Y = 2.
        u(X, Y)?
        '''
        expected_translated_queries = [
            "CREATE TABLE s (z0 TEXT NOT NULL, z1 INT NOT NULL, PRIMARY KEY (z0, z1));",
            "INSERT INTO s VALUES ('x', 1);",
            "INSERT INTO s VALUES ('y', 2);",
            "CREATE VIEW t AS (SELECT s.z1 FROM s WHERE s.z1 > 1);",
            "SELECT * FROM t;",
            "CREATE VIEW u AS (SELECT s.z0, s.z1 FROM s WHERE s.z0 = 'y' AND s.z1 = 2);",
            "SELECT * FROM u;",
        ]
        actual_translated_queries = generate_sql_query_from_datalog_query(datalog_queries)
        for actual_translated_query, expected_translated_query in zip(actual_translated_queries, expected_translated_queries):
            self.assertEqual(actual_translated_query, expected_translated_query)

    def test_complex_comparision_query(self):
        datalog_queries = '''
        s(1, 2).
        s(2, 3).
        s(2, 4).
        s(3, 2).
        s(4, 2).
        t(X, Y) :- s(X, Y), X + Y = 5.
        t(X, Y) :- s(X, Y), X + 2 = 5.
        t(X, Y) :- s(X, Y), Y + 2 = 5.
        t(X, Y)?
        u(X, Y) :- s(X, Y), X > 3.
        u(X, Y)? 
        '''
        expected_translated_queries = [
            'CREATE TABLE s (z0 INT NOT NULL, z1 INT NOT NULL, PRIMARY KEY (z0, z1));',
            'INSERT INTO s VALUES (1, 2);',
            'INSERT INTO s VALUES (2, 3);',
            'INSERT INTO s VALUES (2, 4);',
            'INSERT INTO s VALUES (3, 2);',
            'INSERT INTO s VALUES (4, 2);',
            'CREATE VIEW t AS (SELECT s.z0, s.z1 FROM s WHERE s.z0 + s.z1 = 5) UNION (SELECT s.z0, s.z1 FROM s WHERE s.z0 + 2 = 5) UNION (SELECT s.z0, s.z1 FROM s WHERE s.z1 + 2 = 5);',
            'SELECT * FROM t;',
            'CREATE VIEW u AS (SELECT s.z0, s.z1 FROM s WHERE s.z0 > 3);',
            'SELECT * FROM u;'
        ]
        actual_translated_queries = generate_sql_query_from_datalog_query(datalog_queries)
        for actual_translated_query, expected_translated_query in zip(actual_translated_queries, expected_translated_queries):
            self.assertEqual(actual_translated_query, expected_translated_query)

    def test_timestamp_insertion(self):
        datalog_queries = '''
        s(2019-05-19).
        s(2019-05-19 18:38:00).
        s(2019-05-19T18:39:00).
        s(2019-05-19T18:39:22Z).
        s(2019-05-19T18:40:22+08:00).
        s(X)?
        t(X) :- s(X), X < NOW().
        t(X)?
        '''
        expected_translated_queries = [
            "CREATE TABLE s (z0 TIMESTAMP NOT NULL, PRIMARY KEY (z0));",
            "INSERT INTO s VALUES ('2019-05-19 00:00:00');",
            "INSERT INTO s VALUES ('2019-05-19 18:38:00');",
            "INSERT INTO s VALUES ('2019-05-19 18:39:00');",
            "INSERT INTO s VALUES ('2019-05-19 18:39:22+00:00');",
            "INSERT INTO s VALUES ('2019-05-19 18:40:22+08:00');",
            "SELECT * FROM s;",
            "CREATE VIEW t AS (SELECT s.z0 FROM s WHERE s.z0 < NOW());",
            "SELECT * FROM t;"
        ]
        actual_translated_queries = generate_sql_query_from_datalog_query(datalog_queries)
        for actual_translated_query, expected_translated_query in zip(actual_translated_queries, expected_translated_queries):
            self.assertEqual(actual_translated_query, expected_translated_query)

    def test_support_string_functions(self):
        datalog_queries = '''
        s("X").
        s("Y").
        s(x).
        s(y).
        t(X) :- s(X), X = UPPER(x).
        t(X)?
        u(X) :- s(X), X = LOWER("X").
        u(X)?
        v(X) :- s(X), "X" = UPPER(X).
        v(X)?
        w(X) :- s(X), LOWER(X) = "x".
        w(X)?
        x(X) :- s(X), LOWER(X) = LOWER("X").
        x(X)?
        '''
        expected_translated_queries = [
            "CREATE TABLE s (z0 TEXT NOT NULL, PRIMARY KEY (z0));",
            "INSERT INTO s VALUES ('X');",
            "INSERT INTO s VALUES ('Y');",
            "INSERT INTO s VALUES ('x');",
            "INSERT INTO s VALUES ('y');",
            "CREATE VIEW t AS (SELECT s.z0 FROM s WHERE s.z0 = UPPER('x'));",
            "SELECT * FROM t;",
            "CREATE VIEW u AS (SELECT s.z0 FROM s WHERE s.z0 = LOWER('X'));",
            "SELECT * FROM u;",
            "CREATE VIEW v AS (SELECT s.z0 FROM s WHERE 'X' = UPPER(s.z0));",
            "SELECT * FROM v;",
            "CREATE VIEW w AS (SELECT s.z0 FROM s WHERE LOWER(s.z0) = 'x');",
            "SELECT * FROM w;",
            "CREATE VIEW x AS (SELECT s.z0 FROM s WHERE LOWER(s.z0) = LOWER('X'));",
            "SELECT * FROM x;"
        ]
        actual_translated_queries = generate_sql_query_from_datalog_query(datalog_queries)
        for actual_translated_query, expected_translated_query in zip(actual_translated_queries, expected_translated_queries):
            self.assertEqual(actual_translated_query, expected_translated_query)

    def test_inserting_float(self):
        datalog_queries = '''
        s("X", 1.234).
        s("Y", 2.312).
        '''
        expected_translated_queries = [
            "CREATE TABLE s (z0 TEXT NOT NULL, z1 DECIMAL NOT NULL, PRIMARY KEY (z0, z1));",
            "INSERT INTO s VALUES ('X', 1.234);",
            "INSERT INTO s VALUES ('Y', 2.312);"
        ]
        actual_translated_queries = generate_sql_query_from_datalog_query(datalog_queries)
        for actual_translated_query, expected_translated_query in zip(actual_translated_queries, expected_translated_queries):
            self.assertEqual(actual_translated_query, expected_translated_query)

if __name__ == '__main__':
    unittest.main()