import sqlite3
import ollama
import time

# 1. CONNESSIONE AL DATABASE CHINOOK
conn = sqlite3.connect(r"C:\Users\Andrea\Desktop\Tirocinio\Chinook_Sqlite.sqlite")
cursor = conn.cursor()

# 2. DEFINIZIONE DELLO SCHEMA
schema_db = """
CREATE TABLE "Customer" (
    "CustomerId" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "FirstName" NVARCHAR(40) NOT NULL,
    "LastName" NVARCHAR(20) NOT NULL,
    "Country" NVARCHAR(40),
    "City" NVARCHAR(40),
    "Email" NVARCHAR(60) NOT NULL
);

CREATE TABLE "Invoice" (
    "InvoiceId" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "CustomerId" INTEGER NOT NULL,
    "InvoiceDate" DATETIME NOT NULL,
    "Total" NUMERIC(10,2) NOT NULL,
    FOREIGN KEY ("CustomerId") REFERENCES "Customer" ("CustomerId")
);

CREATE TABLE "InvoiceLine" (
    "InvoiceLineId" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "InvoiceId" INTEGER NOT NULL,
    "TrackId" INTEGER NOT NULL,
    "UnitPrice" NUMERIC(10,2) NOT NULL,
    "Quantity" INTEGER NOT NULL,
    FOREIGN KEY ("InvoiceId") REFERENCES "Invoice" ("InvoiceId"),
    FOREIGN KEY ("TrackId") REFERENCES "Track" ("TrackId")
);

CREATE TABLE "Track" (
    "TrackId" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "Name" NVARCHAR(200) NOT NULL,
    "AlbumId" INTEGER,
    "MediaTypeId" INTEGER NOT NULL,
    "GenreId" INTEGER,
    "Composer" NVARCHAR(220),
    "Milliseconds" INTEGER NOT NULL,
    "Bytes" INTEGER,
    "UnitPrice" NUMERIC(10,2) NOT NULL,
    FOREIGN KEY ("AlbumId") REFERENCES "Album" ("AlbumId"),
    FOREIGN KEY ("GenreId") REFERENCES "Genre" ("GenreId"),
    FOREIGN KEY ("MediaTypeId") REFERENCES "MediaType" ("MediaTypeId")
);
"""

# 3. INPUT UTENTE
print("Benvenuto nel sistema NL2SQL (MODALITÀ TEST METRICHE)!")
frase = input("Fai una domanda: ")

system_prompt = f"""
Sei un traduttore infallibile da linguaggio naturale a query SQL per SQLite.
Usa ESCLUSIVAMENTE questo schema del database per dedurre le relazioni:
{schema_db}

Regole operative ASSOLUTE:
1. Restituisci SOLO la query SQL pura.
2. Usa la notazione Tabella.Colonna (es. Customer.City).
3. Terminata la query SQL con il punto e virgola (;), DEVI FERMARTI.
"""

try:
    print("\nSto elaborando la richiesta con Phi-3 in locale... ")
    
    # --- START CRONOMETRO ---
    start_time = time.time()
    
    response = ollama.chat(
        model="phi3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": frase}
        ]
    )

    # --- STOP CRONOMETRO E SALVATAGGIO METRICHE ---
    end_time = time.time()
    tempo_totale = round(end_time - start_time, 2)
    token_input = response.get('prompt_eval_count', 'N/A')
    token_output = response.get('eval_count', 'N/A')

    sql = response['message']['content'].strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()

    print(f"\n> Query generata dall'AI:\n  {sql}\n")
    
    # STAMPA DELLE METRICHE (Stampate subito, a prescindere dal database!)
    print("="*40)
    print("📊 REPORT METRICHE DI ESECUZIONE REALI")
    print("="*40)
    print(f"⏱️  Tempo di elaborazione AI: {tempo_totale} secondi")
    print(f"📥 Token inviati (Input): {token_input}")
    print(f"📤 Token generati (Output): {token_output}")
    print("="*40 + "\n")

    # ESECUZIONE SUL DATABASE
    if sql.upper().startswith("SELECT"):
        cursor.execute(sql)
        risultati = cursor.fetchall()
        
        print("--- Risultati Estratti ---")
        if risultati:
            for r in risultati[:5]:
                print(" | ".join(str(e) for e in r))
            print("...")
        else:
            print("Nessun record trovato.")
    else:
        print("Errore di Sicurezza: Query non valida.")

except Exception as e:
    print(f"\n[!] Eccezione durante l'esecuzione SQL: {e}")

finally:
    conn.close()