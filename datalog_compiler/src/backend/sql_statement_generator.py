from collections import OrderedDict
from backend.constants import *
from datetime import datetime

COLUMN_PREFIX = "z"

def get_column_name(idx):
    return COLUMN_PREFIX + str(idx)

def get_create_statement(table_name, columns):
    sql_statement = "CREATE TABLE {table_name} (".format(table_name=table_name)
    column_type_statement = []
    for idx, col in enumerate(columns):
        if isinstance(col, int):
            column_type_statement.append(get_column_name(idx) + " INT NOT NULL")
        elif isinstance(col, datetime):
            column_type_statement.append(get_column_name(idx) + " TIMESTAMP NOT NULL")
        else:
            column_type_statement.append(get_column_name(idx) + " TEXT NOT NULL")
    sql_statement += ", ".join(column_type_statement)
    column_name_statement = []
    for idx in range(len(columns)):
        column_name_statement.append(get_column_name(idx))
    sql_statement += ", PRIMARY KEY ({cols_name}));".format(cols_name=", ".join(column_name_statement))
    return sql_statement

def get_insert_statement(table_name, columns):
    sql_statement = "INSERT INTO {table_name} VALUES (".format(table_name=table_name)
    col_values = []
    for column in columns:
        col_values.append(stringify_constants(column))
    sql_statement += "{col_values});".format(col_values=", ".join(col_values))
    return sql_statement

def get_basic_query_statement(table_name, constraints):
    sql_statement = "SELECT * FROM {table_name}".format(table_name=table_name)
    if constraints:
        sql_statement += " WHERE "
        constraints_converted = []
        for idx, val in constraints.items():
            constraints_converted.append(get_column_name(idx) + "=" + stringify_constants(val))
        sql_statement += " AND ".join(constraints_converted)
    sql_statement += ";"
    return sql_statement

def get_drop_view_statement(view_name):
    sql_statement = "DROP VIEW {view_name};".format(view_name=view_name)
    return sql_statement

def create_cols_aligned_dic_and_joins_dic_when_creating_view(view, body, is_recursive):
    cols_alignment_dic = OrderedDict()
    for col in view.cols:
        cols_alignment_dic[col] = None
    joins_dic = {}
    constraints_alignment_dic = {}
    for name, cols in body.table_or_view_name_to_columns_dic.items():
        if view.name == name:
            is_recursive = True
        for idx, col in enumerate(cols):
            if col == "_":
                continue
            if col in joins_dic:
                joins_dic[col].append((name, idx))
            else:
                joins_dic[col] = [(name, idx)]
            if col in cols_alignment_dic and cols_alignment_dic[col] == None:
                cols_alignment_dic[col] = (name, idx)
            if col not in constraints_alignment_dic:
                constraints_alignment_dic[col] = (name, idx)
    return cols_alignment_dic, joins_dic, constraints_alignment_dic, is_recursive

def create_select_statements_when_creating_view(cols_alignment_dic):
    cols = []
    for col_alignment in cols_alignment_dic.values():
        if col_alignment is None:
            # Shouldn't reach here
            raise Exception("Column cannot be aligned")
        table_or_view_name, aligned_col = col_alignment
        cols.append("{table_or_view_name}.{col_name}".format(
            table_or_view_name=table_or_view_name,
            col_name=get_column_name(aligned_col)
        ))
    return "SELECT {cols}".format(cols = ", ".join(cols))

def stringify_constants(constant, add_quotes=True):
    if (isinstance(constant, str) or isinstance(constant, datetime)) and add_quotes:
        return "'" + str(constant) + "'"
    return str(constant)

def process_left_or_right_term_key_and_value(left_or_right_term_key, left_or_right_term_value, constraints_alignment_dic):
    if left_or_right_term_key == VAR_KEY:
        table_to_join_to, idx_to_join_to = constraints_alignment_dic[left_or_right_term_value]
        return "{table_to_join_to}.{col_to_join_to}".format(table_to_join_to=table_to_join_to, col_to_join_to=get_column_name(idx_to_join_to))
    elif left_or_right_term_key == CONSTANT_KEY:
        return stringify_constants(left_or_right_term_value)
    raise Exception("Unsupported Term")

def process_left_or_right_term(constraints_alignment_dic, left_or_right_term):
    if not isinstance(left_or_right_term, tuple):
        if left_or_right_term in {'+', '-', '*', '/'}:
            return stringify_constants(left_or_right_term, add_quotes=False)
        raise Exception("Unsupported Term")
    if left_or_right_term[0] == FUNC_KEY:
        function_name, args = left_or_right_term[1:]
        return "{function_name}({args})".format(function_name=function_name, args=", ".join([process_left_or_right_term_key_and_value(arg[0], arg[1], constraints_alignment_dic) for arg in args]))
    left_or_right_term_key, left_or_right_term_value = left_or_right_term
    return process_left_or_right_term_key_and_value(left_or_right_term_key, left_or_right_term_value, constraints_alignment_dic)

def create_where_statement_when_creating_view(joins_dic, constraints_alignment_dic, constraints):
    where_conditions = []
    for join in joins_dic.values():
        table_to_join_to, idx_to_join_to = join[0]
        for idx in range(1, len(join)):
            joining_table, joining_idx = join[idx]
            where_conditions.append("{table_to_join_to}.{col_to_join_to}={joining_table}.{joining_col}".format(
                table_to_join_to=table_to_join_to,
                col_to_join_to=get_column_name(idx_to_join_to),
                joining_table=joining_table,
                joining_col=get_column_name(joining_idx)
            ))
    for constraint in constraints:
        constraint_statement = " ".join([process_left_or_right_term(constraints_alignment_dic, l) for l in constraint.left] + [constraint.operator] + [process_left_or_right_term(constraints_alignment_dic, r) for r in constraint.right])
        where_conditions.append(constraint_statement)
    if where_conditions:
        return "WHERE {joins}".format(joins=" AND " .join(where_conditions))
    return ""

def process_body_when_creating_view(view, body, is_recursive):
    cols_alignment_dic, joins_dic, constraints_alignment_dic, is_recursive = create_cols_aligned_dic_and_joins_dic_when_creating_view(view, body, is_recursive)
    select_statement = create_select_statements_when_creating_view(cols_alignment_dic)
    joined_statement = "FROM {joined_table}".format(joined_table=", ".join(body.table_or_view_name_to_columns_dic.keys()))
    where_statement = create_where_statement_when_creating_view(joins_dic, constraints_alignment_dic, body.constraints)
    if where_statement:
        body_converted = "({select_statement} {joined_statement} {where_statement})".format(
            select_statement=select_statement,
            joined_statement=joined_statement,
            where_statement=where_statement
        )
    else:
        body_converted = "({select_statement} {joined_statement})".format(
            select_statement=select_statement,
            joined_statement=joined_statement,
            where_statement=where_statement
        )
    return body_converted, is_recursive

def create_view_statement(view):
    is_recursive = False
    bodies_converted = []
    for body in view.body_processed_results:
        body_converted, is_recursive = process_body_when_creating_view(view, body, is_recursive)
        bodies_converted.append(body_converted)
    if is_recursive:
        cols = [get_column_name(idx) for idx in range(len(view.cols))]
        sql_statement = "CREATE VIEW {view_name} AS WITH RECURSIVE {view_name} ({cols}) AS ({main_body}) SELECT * FROM {view_name};".format(view_name=view.name, cols=", ".join(cols), main_body=" UNION DISTINCT ".join(bodies_converted))
    else:
        sql_statement = "CREATE VIEW {view_name} AS {main_body};".format(view_name=view.name, main_body=" UNION ".join(bodies_converted)) 
    return sql_statement
