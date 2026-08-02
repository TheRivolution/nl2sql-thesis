import sqlite3 

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clienti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    citta TEXT
)
""")

cursor.execute("SELECT COUNT(*) FROM clienti")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO clienti (nome, citta) VALUES (?, ?)", ("Andrea", "Lecce"))
    cursor.execute("INSERT INTO clienti (nome, citta) VALUES (?, ?)", ("Marco", "Roma"))
    cursor.execute("INSERT INTO clienti (nome, citta) VALUES (?, ?)", ("Luca", "Milano"))
    conn.commit()

frase = input("Scrivi la tua richiesta: ")

if frase.lower() == "clienti di roma":
    sql = "SELECT * FROM clienti WHERE citta='Roma'"
elif frase.lower() == "clienti di milano":
    sql = "SELECT * FROM clienti WHERE citta='Milano'"
else:
    sql = "SELECT * FROM clienti"

print("Input dell'utente:", frase)
print("Query SQL generata:", sql)

cursor.execute(sql)
risultati = cursor.fetchall()

for r in risultati:
    print(r)

conn.close()