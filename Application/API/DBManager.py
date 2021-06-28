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
            sql_string = f'CREATE TABLE IF NOT EXISTS {table_name} ( {", ".join(formatted_array)} );'
            c.execute(sql_string)
        except Exception as e:
            print(e)

    def get_colnames(self, table):
        """
        Get column names from table
        :param table: table name
        :return: list column names
        """
        cur = self.conn.execute(f'SELECT * FROM {table}')
        desc = cur.description
        colnames = [r[0] for r in desc]
        return colnames

    def get_first_row(self, table):
        """
        Get first row from table (e.g. get main character)
        :param table: table name
        :return: tuple row
        """
        sql = f'SELECT * FROM {table} ORDER BY ROWID ASC LIMIT 1'
        cur = self.conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        return row

    def insert_row(self, table, row):
        """
        Create a new row
        :param table: string table name
        :param row: tuple row values
        :return: int row id
        """

        sql = f'INSERT INTO {table}({",".join(self.get_colnames(table))}) VALUES{row}'
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

        return cur.lastrowid

    def update_row(self, table, id, body):
        """
        Update a row given its id
        :param table: string table name
        :param id: int id
        :param body: update dict (key = column, value = update value)
        :return: int row id
        """
        formatted_body_array = [f'{f} = "{body[f]}"' for f in body]
        formatted_body_string = ', '.join(formatted_body_array)
        sql = f'UPDATE {table} SET {formatted_body_string} WHERE id = {id}'
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        return id

    def delete_rows(self, table, ids):
        """
        Delete a row given its id
        :param table: string table name
        :param id: list (int) ids
        :return: None
        """
        if ids[0] == '*':
            sql = f'DELETE FROM {table}'
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
        else:
            for id in ids:
                sql = f'DELETE FROM {table} WHERE id = {id}'
                cur = self.conn.cursor()
                cur.execute(sql)
                self.conn.commit()

    def get_id(self, table, name):
        sql = f'SELECT * FROM {table} WHERE name LIKE "{name}"'
        cur = self.conn.cursor()
        cur.execute(sql)
        return_row = cur.fetchone()
        if return_row:
            return return_row[0]
        return None


# # Testing Section
# db = DBManager(r'F:\Phil Elder\Projects\Python\grove\Testing\saves.db')

# fields = [{
#     'name': 'id',
#     'type': 'int',
#     'meta': 'PRIMARY KEY'
# }, {
#     'name': 'name',
#     'type': 'str',
#     'meta': 'NULL'
# }, {
#     'name': 'flaps',
#     'type': 'str',
#     'meta': 'NULL'
# }]

# db.create_table('test', fields)
# # print(db.insert_row('test', (4, 'second rowwww!', 'skitle')))
# print(db.get_first_row('test'))

# 


# db.delete_rows('test', ['*'])

# print(db.insert_row('test', (1, 'first row!', 1)))
# print(db.insert_row('test', (2, 'firssssst row!', 1)))

# db.delete_rows('test', [1])

# # print(db.get_id('test', 'second row'))


# # db.delete_row('test', 2)

# # update_dict = {
# #     'name': 'flapskittlessss',
# #     'priority': 9
# # }
# # db.update_row('test', 2, update_dict)

# cursor = db.conn.execute('select * from test')
# print(cursor.fetchall())

