import sqlite3

class DBManager:
    def __init__(self, file):
        self.conn = self.create_connection(file)

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :string db_file: database file
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
        :obj conn: Connection object
        :string table_name: a table name
        :list fields: list of field objects (keys: name (str), type (str), meta (str))
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
        :string table: table name
        :return: list column names
        """
        cur = self.conn.execute(f'SELECT * FROM {table}')
        desc = cur.description
        colnames = [r[0] for r in desc]
        return colnames

    def get_first_row(self, table):
        """
        Get first row from table (e.g. get main character)
        :string table: table name
        :return: tuple row
        """
        sql = f'SELECT * FROM {table} ORDER BY ROWID ASC LIMIT 1'
        cur = self.conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        return row

    def get_row_by_id(self, table, id):
        """
        Get a row from a table given the table name and id
        :string table: table name
        :int id: row id
        :return: tuple row
        """
        sql = f'SELECT * FROM {table} WHERE ID = {id}'
        cur = self.conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        return row

    def get_all_rows(self, table):
        """
        Get all rows from a table
        :string table: table name
        :return: tuple of tuples rows
        """
        sql = f'SELECT * FROM {table}'
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    def get_row_count(self, table):
        """
        Get a count of all rows in table
        :string table: table name
        :return: int row count
        """
        sql = f'SELECT * FROM {table}'
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return len(rows)

    def get_associated_items(self, table, field, id):
        """
        get a list of rows from a table given a field and a value (e.g. get all items on a map)
        :string table: table name
        :string field: table field for id
        :int id: row id
        :return: tuple row
        """
        sql = f'SELECT * FROM {table} WHERE {field} = {id}'
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    def get_next_game_id(self):
        """
        Get the lowest available game ID
        :return: int id
        """
        sql = f'SELECT * FROM Games ORDER BY ROWID DESC'
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        counter = 1
        for row in rows:
            if row[0] != counter:
                return counter
            counter += 1

    
    def get_next_id(self, table):
        """
        Get the next ID to be used for a table
        :string table: table name
        :return: int id
        """
        sql = f'SELECT * FROM {table} ORDER BY ROWID DESC LIMIT 1'
        cur = self.conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            return row[0] + 1
        return 1

    def insert_row(self, table, row):
        """
        Create a new row
        :string table: string table name
        :tuple row: tuple row values
        :return: int row id
        """
        insert_str = f'({",".join(["?" for i in row])})'
        sql = f'INSERT INTO {table}({",".join(self.get_colnames(table))}) VALUES{insert_str}'
        cur = self.conn.cursor()
        cur.execute(sql, row)
        self.conn.commit()

        return cur.lastrowid

    def update_row(self, table, id, body):
        """
        Update a row given its id
        :string table: string table name
        :int id: int id
        :dict body: update dict (key = column, value = update value)
        :return: int row id
        """
        formatted_body_array = [f'{f} = "{body[f]}"' for f in body]
        formatted_body_string = ', '.join(formatted_body_array)
        sql = f'UPDATE {table} SET {formatted_body_string} WHERE id = {id}'
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        return id

    def delete_rows(self, table, ids, custom_field=None):
        """
        Delete a row given its id
        :string table: string table name
        :int id: list (int) ids
        :custom_field: string non-id field to check against (optional, default None)
        :return: None
        """
        field = custom_field if custom_field else 'id'
        if len(ids) > 0 and ids[0] == '*':
            sql = f'DELETE FROM {table}'
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
        else:
            for id in ids:
                sql = f'DELETE FROM {table} WHERE {field} = {id}'
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
# db = DBManager(r'C:\Projects\grove\Application\Database\main.db')
# print(db.get_row_count('Items'))

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

