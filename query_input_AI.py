import sqlite3
import ollama

# 1. CONNESSIONE AL DATABASE CHINOOK - Ci colleghiamo direttamente al file che ho scaricato. 
conn = sqlite3.connect("Chinook_Sqlite.sqlite")
cursor = conn.cursor()

# 2. DEFINIZIONE DELLO SCHEMA (PROMPT ENGINEERING)
# Passiamo a Phi-3 lo schema relazionale a 4 tabelle per permettere navigazioni complesse (Multi-JOIN).
schema_db = """
CREATE TABLE "Customer" ( -- Anagrafica clienti
    "CustomerId" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "FirstName" NVARCHAR(40) NOT NULL,
    "LastName" NVARCHAR(20) NOT NULL,
    "Country" NVARCHAR(40),
    "City" NVARCHAR(40),
    "Email" NVARCHAR(60) NOT NULL
);

CREATE TABLE "Invoice" ( -- Fatture e ordini di acquisto
    "InvoiceId" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "CustomerId" INTEGER NOT NULL,
    "InvoiceDate" DATETIME NOT NULL,
    "Total" NUMERIC(10,2) NOT NULL,
    FOREIGN KEY ("CustomerId") REFERENCES "Customer" ("CustomerId")
);

CREATE TABLE "InvoiceLine" ( -- Dettaglio della singola riga di fattura
    "InvoiceLineId" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "InvoiceId" INTEGER NOT NULL,
    "TrackId" INTEGER NOT NULL,
    "UnitPrice" NUMERIC(10,2) NOT NULL,
    "Quantity" INTEGER NOT NULL,
    FOREIGN KEY ("InvoiceId") REFERENCES "Invoice" ("InvoiceId"),
    FOREIGN KEY ("TrackId") REFERENCES "Track" ("TrackId")
);

CREATE TABLE "Track" ( -- Catalogo dei brani musicali / canzoni acquistabili
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
print("Benvenuto nel sistema NL2SQL!")
frase = input("Fai una domanda: ")

# 4. COSTRUZIONE DEL SYSTEM PROMPT (La personalità dell'IA)
# Spieghiamo all'IA chi è e come deve ragionare con lo schema
system_prompt = f"""
Sei un traduttore infallibile da linguaggio naturale a query SQL per SQLite.
Usa ESCLUSIVAMENTE questo schema del database per dedurre le relazioni:
{schema_db}

Regole operative ASSOLUTE:
1. Restituisci SOLO la query SQL pura, senza formattazione Markdown (NON scrivere ```sql).
2. Usa la notazione Tabella.Colonna (es. Customer.City) per evitare ambiguità.
3. FONDAMENTALE: Se applichi un filtro (WHERE) su una colonna, assicurati SEMPRE che la tabella che contiene quella colonna sia inclusa nelle JOIN!
4. Terminata la query SQL con il punto e virgola (;), DEVI FERMARTI. Non aggiungere note, spiegazioni o altri prompt.
"""

# 5. CHIAMATA ALL'INTELLIGENZA ARTIFICIALE (IN LOCALE)
try:
    print("\nSto elaborando la richiesta con Phi-3 in locale... 🧠")
    
    # Invece di un solo messaggio, usiamo il "System" per le regole e lo "User" per la frase
    response = ollama.chat(
        model="phi3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": frase}
        ]
    )

    # 6. PARSING E PULIZIA DELL'OUTPUT
    sql = response['message']['content'].strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()

    print(f"> Query generata dall'AI:\n  {sql}\n")

    # 7. CONTROLLO DI SICUREZZA E ESECUZIONE
    if sql.upper().startswith("SELECT"):
        cursor.execute(sql)
        risultati = cursor.fetchall()

        print("--- Risultati Estratti ---")
        if risultati:
            # Stampiamo SOLO i primi 10 risultati per non intasare lo schermo
            for r in risultati[:10]:
                riga_formattata = " | ".join(str(elemento) for elemento in r)
                print(riga_formattata)
            
            # Se ci sono più di 10 risultati, avvisiamo l'utente
            if len(risultati) > 10:
                print(f"... e altri {len(risultati) - 10} record (Totale estratti: {len(risultati)}).")
        else:
            print("Nessun record corrispondente trovato nel database.")
            
        # Ristampiamo la query alla fine così non la perdi nello scroll dello schermo!
        print(f"\n✅ [COMPLETATO] Query eseguita con successo:\n{sql}")
            
    else:
        print("🛑 Errore di Sicurezza: La richiesta non è valida o non è una query di sola lettura (SELECT).")

except Exception as e:
    print(f"\n❌ Si è verificato un errore di sistema: {e}")
    print("💡 Assicurati che l'icona di Ollama sia attiva e che il file Chinook_Sqlite.sqlite sia nella stessa cartella.")

finally:
    # 8. CHIUSURA DELLE CONNESSIONI
    conn.close()