import sqlite3

class DBManager:
    def __init__(self, file):
        self.conn = self.create_connection(file)

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Exception as e:
            print(e)

        return conn

    def create_table(self, table_name, fields):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param table_name: a table name
        :param fields: list of field objects (keys: name (str), type (str), meta (str))
        :meta values: PRIMARY KEY, NOT NULL, NULL
        :return:
        """
        try:
            c = self.conn.cursor()
            formatted_array = [f'{f["name"]} {f["type"]} {f["meta"]}' for f in fields]
            print(formatted_array)
            sql_string = f'CREATE TABLE IF NOT EXISTS {table_name} ( {", ".join(formatted_array)} );'
            print(sql_string)
            c.execute(sql_string)
        except Exception as e:
            print(e)