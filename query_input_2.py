import sqlite3 

# Connessione e tabella
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clienti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    citta TEXT
)
""")

# Inserimento dati di esempio
cursor.execute("SELECT COUNT(*) FROM clienti")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO clienti (nome, citta) VALUES (?, ?)", ("Andrea", "Lecce"))
    cursor.execute("INSERT INTO clienti (nome, citta) VALUES (?, ?)", ("Marco", "Roma"))
    cursor.execute("INSERT INTO clienti (nome, citta) VALUES (?, ?)", ("Luca", "Milano"))
    conn.commit()

frase = input("Scrivi la tua richiesta: ").lower()

# Dizionario parole chiave → query
keyword_sql = {
    "roma": "SELECT * FROM clienti WHERE citta='Roma'",
    "milano": "SELECT * FROM clienti WHERE citta='Milano'",
    "lecce": "SELECT * FROM clienti WHERE citta='Lecce'"
}

# Cerca parole chiave nella frase
sql = "SELECT * FROM clienti"  # default
for parola, query in keyword_sql.items():
    if parola in frase:
        sql = query
        break

cursor.execute(sql)
risultati = cursor.fetchall()

for r in risultati:
    print(r)

conn.close()