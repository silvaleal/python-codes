import sqlite3

# Um simples autoloader que irá preparar o seu banco de dados de forma automatica.
# É perfeito para projetos pequenos.

dbTables = [
    '''
    CREATE TABLE IF NOT EXISTS todolist (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title VARCHAR(30) NOT NULL,
        deadline DATETIME,
        added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        removed_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );'''
]

class LoaderDB:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.tables()

    def tables(self):
        for table in dbTables:
            self.cursor.execute(table)