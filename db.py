import sqlite3


class Db:

    def connect_db(self):
        con = sqlite3.connect('main.db')
        return con

    def create_table(self):
        con = self.connect_db()
        cursor = con.cursor()
        cursor.execute(f'CREATE TABLE IF NOT EXISTS win_count('
                       f'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                       f'name TEXT NOT NULL,'
                       'win INTEGER DEFAULT 0 NOT NULL '
                       f')')
        con.commit()
        con.close()

    def insert_db(self, name, win):
        con = self.connect_db()
        cursor = con.cursor()
        cursor.execute(f'INSERT INTO win_count (name, win) VALUES(?,?)', (name, win))
        con.commit()
        con.close()

    def get_data(self, name):
        con = self.connect_db()
        cursor = con.cursor()
        data = cursor.execute(f'SELECT COUNT(*) FROM win_count WHERE name = "{name}"').fetchall()

        return data[0][0]


