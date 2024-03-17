from backend.sql_statement import get_create_and_insert_statement, get_insert_statement
from common.node_names import *

class Interpreter:
    def __init__(self):
        self.table_names = set()

    def get_node_name(self, tup):
        return tup[0]

    def get_value(self, node_val, tup, idx=1):
        assert tup[0] == node_val
        return tup[idx]

    def check_value_of_statement(self, statement):
        if self.get_node_name(statement) == ASSERTION_NODE:
            return "CREATE_AND_INSERT"
        return "UNSUPPORTED_STATEMENT"

    def traverse_and_get_value(self, list_of_node_names, node, list_of_idx=None):
        node_val = node
        for idx, node_name in enumerate(list_of_node_names):
            if list_of_idx is not None:
                node_val = self.get_value(node_name, node_val, list_of_idx[idx])
            else:
                node_val = self.get_value(node_name, node_val)
        return node_val

    def interpret_create_and_insert_statement(self, statement):
        table_name = self.traverse_and_get_value(
            [ASSERTION_NODE, CLAUSE_NODE, LITERAL_NODE, PREDICATE_NODE],
            statement
        )
        terms = self.traverse_and_get_value(
            [ASSERTION_NODE, CLAUSE_NODE, LITERAL_NODE, TERMS_NODE],
            statement,
            [1, 1, 3, 1]
        )
        columns = []
        for term in terms:
            columns.append(self.traverse_and_get_value([TERM_NODE, CONSTANT_NODE], term))
        if table_name in self.table_names:
            return get_insert_statement(table_name, columns)
        self.table_names.add(table_name)
        return get_create_and_insert_statement(table_name, columns)

    def interpret_statements(self, statements):
        sql_translations = []
        for statement_node, statement in statements:
            assert statement_node == STATEMENT_NODE
            type_of_statement = self.check_value_of_statement(statement)
            if type_of_statement == "CREATE_AND_INSERT":
                sql_translations.extend(self.interpret_create_and_insert_statement(statement))
            else:
                raise Exception("Unsupported statement")
        return sql_translations

    def interpret(self, ast):
        assert self.get_node_name(ast) == PROGRAM_NODE
        return self.interpret_statements(ast[1])
