COLUMN_PREFIX = "z"

def get_create_statement(table_name, columns):
    sql_statements = []
    sql_statement = "CREATE TABLE {table_name} (".format(table_name=table_name)
    for idx in range(len(columns)):
        sql_statement += COLUMN_PREFIX + str(idx) + " TEXT NONNULL,"
    sql_statement += " PRIMARY KEY ("
    for idx in range(len(columns)):
        if idx == len(columns) - 1:
            postfix = ")"
        else:
            postfix = ", "
        sql_statement += COLUMN_PREFIX + str(idx) + postfix
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