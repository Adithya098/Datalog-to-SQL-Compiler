from collections import OrderedDict

COLUMN_PREFIX = "z"

def get_column_name(idx):
    return COLUMN_PREFIX + str(idx)

def get_create_statement(table_name, columns):
    sql_statements = []
    sql_statement = "CREATE TABLE {table_name} (".format(table_name=table_name)
    for idx in range(len(columns)):
        sql_statement += get_column_name(idx) + " TEXT NOT NULL,"
    sql_statement += " PRIMARY KEY ("
    for idx in range(len(columns)):
        if idx == len(columns) - 1:
            postfix = ")"
        else:
            postfix = ", "
        sql_statement += get_column_name(idx) + postfix
    sql_statement += ");"
    sql_statements.append(sql_statement)
    return sql_statements

def get_insert_statement(table_name, columns):
    sql_statements = []
    sql_statement = "INSERT INTO {table_name} VALUES (".format(table_name=table_name)
    for idx, column in enumerate(columns):
        if idx == len(columns) - 1:
            postfix = ");"
        else:
            postfix = ", "
        sql_statement += "'" + column + "'" + postfix
    sql_statements.append(sql_statement)
    return sql_statements

def get_create_and_insert_statement(table_name, columns):
    sql_statements = []
    sql_statements.extend(get_create_statement(table_name, columns))
    sql_statements.extend(get_insert_statement(table_name, columns))
    return sql_statements

def get_basic_query_statement(table_name, constraints):
    sql_statements = []
    sql_statement = "SELECT * FROM {table_name}".format(table_name=table_name)
    if constraints:
        sql_statement += " WHERE "
        constraints_converted = []
        for idx, val in constraints.items():
            constraints_converted.append(get_column_name(idx) + "=" + "'" + str(val) + "'")
        sql_statement += " AND ".join(constraints_converted)
    sql_statement += ";"
    sql_statements.append(sql_statement)
    return sql_statements

def get_drop_view_statement(view_name):
    sql_statements = []
    sql_statement = "DROP VIEW {view_name}".format(view_name=view_name)
    sql_statements.append(sql_statement)
    return sql_statements

def create_cols_aligned_dic_and_joins_dic_when_creating_view(view, body, is_recursive):
    cols_alignment_dic = OrderedDict()
    for col in view.cols:
        cols_alignment_dic[col] = None
    joins_dic = {}
    for name, cols in body.items():
        if view.name == name:
            is_recursive = True
        for idx, col in enumerate(cols):
            if col in joins_dic:
                joins_dic[col].append((name, idx))
            else:
                joins_dic[col] = [(name, idx)]
            if col in cols_alignment_dic and cols_alignment_dic[col] == None:
                cols_alignment_dic[col] = ((name, idx))
    return cols_alignment_dic, joins_dic, is_recursive

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

def create_where_statement_when_creating_view(joins_dic):
    join_conditions = []
    for join in joins_dic.values():
        table_to_join_to, idx_to_join_to = join[0]
        for idx in range(1, len(join)):
            joining_table, joining_idx = join[idx]
            join_conditions.append("{table_to_join_to}.{col_to_join_to}={joining_table}.{joining_col}".format(
                table_to_join_to=table_to_join_to,
                col_to_join_to = get_column_name(idx_to_join_to),
                joining_table=joining_table,
                joining_col = get_column_name(joining_idx)
            ))
    if join_conditions:
        return "WHERE {joins}".format(joins=", " .join(join_conditions))
    return ""

def process_body_when_creating_view(view, body, is_recursive):
    cols_alignment_dic, joins_dic, is_recursive = create_cols_aligned_dic_and_joins_dic_when_creating_view(view, body, is_recursive)
    select_statement = create_select_statements_when_creating_view(cols_alignment_dic)
    joined_statement = "FROM {joined_table}".format(joined_table=", ".join(body.keys()))
    where_statement = create_where_statement_when_creating_view(joins_dic)
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
    sql_statements = []
    is_recursive = False
    bodies_converted = []
    for body in view.bodies:
        body_converted, is_recursive = process_body_when_creating_view(view, body, is_recursive)
        bodies_converted.append(body_converted)
    if is_recursive:
        cols = [get_column_name(idx) for idx in range(len(view.cols))]
        sql_statement = "CREATE RECURSIVE VIEW {view_name} ({cols}) AS {main_body};".format(view_name=view.name, cols=", ".join(cols), main_body=" UNION ".join(bodies_converted))
    else:
        sql_statement = "CREATE VIEW {view_name} AS {main_body};".format(view_name=view.name, main_body=" UNION ".join(bodies_converted)) 
    sql_statements.append(sql_statement)
    return sql_statements
