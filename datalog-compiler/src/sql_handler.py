import psycopg2
import traceback

class SQLHandler:
    def __init__(self, conn):
        """
        Initializes the SQLHandler with a database connection.
        """
        self.conn = conn

    def reload_sql_file(self, file_path):
        """
        Reloads the SQL file into the PostgreSQL instance.

        Args:
        - file_path (str): The path to the SQL file to be reloaded.
        """
        try:
            with open(file_path, 'r') as sql_file:
                sql_commands = sql_file.read().split(';')
                cur = self.conn.cursor()
                for command in sql_commands:
                    cur.execute(command)
                self.conn.commit()
                cur.close()
            print("SQL file reloaded successfully.")
        except Exception as e:
            print("Error reloading SQL file:", e)

    def execute_sql_query(self, sql_query):
        """
        Executes a given SQL query.

        Args:
        - sql_query (str): The SQL query to execute.
        """
        try:
            cur = self.conn.cursor()
            cur.execute(sql_query)
            self.conn.commit()
            cur.close()
        except Exception as e:
            self.conn.rollback()  
            print("Error executing SQL query:", e)

    def drop_all_objects(self):
        """
        Drops all tables, views, sequences, and functions associated with the current database.
        """
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'")
            tables = cur.fetchall()
            for table in tables:
                cur.execute(f"DROP TABLE IF EXISTS {table[0]} CASCADE")

            cur.execute("SELECT viewname FROM pg_views WHERE schemaname='public'")
            views = cur.fetchall()
            for view in views:
                cur.execute(f"DROP VIEW IF EXISTS {view[0]} CASCADE")

            cur.execute("SELECT sequence_name FROM information_schema.sequences WHERE sequence_schema='public'")
            sequences = cur.fetchall()
            for sequence in sequences:
                cur.execute(f"DROP SEQUENCE IF EXISTS {sequence[0]} CASCADE")

            cur.execute("SELECT proname FROM pg_proc WHERE pronamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')")
            functions = cur.fetchall()
            for function in functions:
                cur.execute(f"DROP FUNCTION IF EXISTS {function[0]} CASCADE")

            self.conn.commit()
            cur.close()
            print("All objects dropped successfully.")
        except Exception as e:
            self.conn.rollback()
            print("Error dropping objects:", e)
