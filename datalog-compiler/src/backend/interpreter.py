from backend.sql_statement import get_create_and_insert_statement

def get_node_name(tup):
    return tup[0]

def get_value(node_val, tup, idx=1):
    assert tup[0] == node_val
    return tup[idx]

def check_value_of_statement(statement):
    if get_node_name(statement) == 'assertion':
        return "CREATE_AND_INSERT"
    return "UNSUPPORTED_STATEMENT"

def traverse_and_get_value(list_of_node_names, node, list_of_idx=None):
    node_val = node
    for idx, node_name in enumerate(list_of_node_names):
        if list_of_idx is not None:
            node_val = get_value(node_name, node_val, list_of_idx[idx])
        else:
            node_val = get_value(node_name, node_val)
    return node_val

def interpret_create_and_insert_statement(statement):
    table_name = traverse_and_get_value(
        ['assertion', 'clause', 'literal', 'predicate'],
        statement
    )
    terms = traverse_and_get_value(
        ['assertion', 'clause', 'literal', 'terms'],
        statement,
        [1, 1, 3, 1]
    )
    columns = []
    for term in terms:
        columns.append(traverse_and_get_value(['term', 'constant'], term))
    return get_create_and_insert_statement(table_name, columns)

def interpret_statements(statements):
    sql_translations = []
    for statement_node, statement in statements:
        assert statement_node == 'statement'
        type_of_statement = check_value_of_statement(statement)
        if type_of_statement == "CREATE_AND_INSERT":
            sql_translations.extend(interpret_create_and_insert_statement(statement))
        else:
            raise Exception("Unsupported statement")
    return sql_translations

def interpret(ast):
    assert get_node_name(ast) == 'program'
    return interpret_statements(ast[1])
