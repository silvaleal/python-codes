import sqlite3

# Um autoloader mais robústo, irá preparar o seu banco de dados de forma automatica.
# É possível colocar seeders e facilitar mais ainda a criação do banco de dados.

class Loader:
    def __init__(self):
        self.connection = sqlite3.connect('database')
        self.cursor = self.connection.cursor()
        self.run()
        
    def tables(self): # Querys que serão utilizadas ao preparar o banco de dados
        # Use apenas CREATE TABLE caso a tabela tenha seeders.
        return {
            "user": """CREATE TABLE user (
                axe_level INT DEFAULT 1,
                coins INTEGER DEFAULT 0
                );""",
                
            "items": """CREATE TABLE items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(45) NOT NULL,
                price INTEGER NOT NULL
                );""",
            
            # Como o inventory não tem seeders, posso usar o IF NOT EXISTS
            "inventory": """CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                quantify INTEGER NOT NULL
                );"""
        }
        
    def seeders(self): # Os valores que serão criados no momento em que a tabela for criada.
        return {
            "items": [
                {
                    "name": "oak_wood",
                    "price": 1
                },
                {
                    "name": "spruce_wood",
                    "price": 2
                },
                {
                    "name": "dark_oak_wood",
                    "price": 3
                }
            ],
            "user": [
                {
                    "axe_level": 1,
                    "coins": 0
                }
            ]
        }
        
    def run(self):
        for table in self.tables():
            try:
                self.cursor.execute(self.tables()[table])
                
                totalFields = []
                totalValues = []
                
                seeders = self.seeders()
                if not table in seeders: continue
                
                for fields in seeders[table]:
                    for field in fields:
                        
                        valueFormated = f'"{fields[field]}"' if type(fields[field]) == str else f'{fields[field]}' # Formatando o values pro query
                        
                        if field in totalFields:
                            totalFields = []
                            totalValues = []
                            totalValues.append(valueFormated)
                            totalFields.append(field)
                        else:
                            totalValues.append(valueFormated)
                            totalFields.append(field)
                    query = f"INSERT INTO {table} ({', '.join(totalFields)}) VALUES ({', '.join(totalValues)})"
                    self.cursor.execute(query)
                    self.connection.commit()
                
            except sqlite3.OperationalError as error:
                if "already exists" in str(error):
                    print(f"[!] Tabela {table} foi encontrada")
                else:
                    print(error)
