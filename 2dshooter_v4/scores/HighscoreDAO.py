import sqlite3

class HighscoreDAO():
    def __init__(self):
        self.db = sqlite3.connect("scores/HighscoreDB.db")
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users(name TEXT UNIQUE,zeit TEXT, datum TEXT)")

    def insert(self,name,zeit,datum):
        self.cursor.execute('''INSERT INTO users(name, zeit, datum)
                          VALUES(:name,:zeit, :datum)''',
                       {'name': name, 'zeit': zeit, 'datum': datum})
        self.db.commit()
    def get_all_data(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()


