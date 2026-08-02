# NL2SQL - Da Linguaggio Naturale a SQL

Prototipo sviluppato come **Tesi di Laurea in Ingegneria Informatica** presso l'Università del Salento.

Il sistema traduce domande poste in linguaggio naturale in query SQL eseguibili, utilizzando un modello linguistico (LLM) eseguito in locale tramite **Ollama**, senza dipendere da API cloud esterne.

**Relatori:** Prof. Manni, Prof. Ghiani

---

## Come funziona

1. L'utente scrive una domanda in linguaggio naturale (es. "quali sono i 5 clienti che hanno speso di più?")
2. Al modello LLM viene fornito lo schema del database (DDL) come contesto
3. Il modello genera la query SQL corrispondente
4. La query viene eseguita automaticamente sul database SQLite
5. Il risultato viene mostrato all'utente

Il database utilizzato per i test è **Chinook** (`Chinook_Sqlite.sqlite`), un database relazionale di esempio che simula uno store musicale (clienti, ordini, brani, album, artisti).

## Stack tecnologico

- **Python** - logica applicativa e pipeline
- **Ollama** - esecuzione locale del modello LLM
- **SQLite** - database di test (Chinook)

## Come avviarlo

Requisiti:
- Python 3.x installato
- [Ollama](https://ollama.com) installato e in esecuzione in locale, con un modello scaricato (es. `ollama pull phi3`)

Avvio:

```bash
python query_input_AI.py
```

Lo script chiede una domanda in linguaggio naturale, genera la query SQL corrispondente tramite il modello LLM locale, la esegue sul database Chinook e restituisce il risultato.

## Esempio

> **Domanda:** _[esempio da inserire]_
>
> **Query SQL generata:**
> ```sql
> [esempio da inserire]
> ```
>
> **Risultato:** _[esempio da inserire]_

## Limiti del prototipo

Durante lo sviluppo sono state osservate alcune criticità tipiche di questo approccio:
- Possibili allucinazioni del modello su schemi complessi o domande ambigue
- Sensibilità alla formulazione della domanda (query diverse per domande semanticamente equivalenti)
- Dipendenza dalla qualità del modello LLM utilizzato in locale

---

# NL2SQL - Natural Language to SQL

Prototype developed as a **Bachelor's Thesis in Computer Engineering** at the University of Salento (Università del Salento).

The system translates natural language questions into executable SQL queries, using a language model (LLM) running locally via **Ollama**, with no dependency on external cloud APIs.

**Advisors:** Prof. Manni, Prof. Ghiani

---

## How it works

1. The user writes a question in natural language (e.g. "who are the top 5 customers by spending?")
2. The database schema (DDL) is provided to the LLM as context
3. The model generates the corresponding SQL query
4. The query is automatically executed on the SQLite database
5. The result is returned to the user

The test database is **Chinook** (`Chinook_Sqlite.sqlite`), a sample relational database simulating a digital music store (customers, orders, tracks, albums, artists).

## Tech stack

- **Python** - application logic and pipeline
- **Ollama** - local LLM execution
- **SQLite** - test database (Chinook)

## How to run it

Requirements:
- Python 3.x installed
- [Ollama](https://ollama.com) installed and running locally, with a model pulled (e.g. `ollama pull phi3`)

Run:

```bash
python query_input_AI.py
```

The script prompts for a natural language question, generates the corresponding SQL query via the local LLM, executes it on the Chinook database, and returns the result.

## Example

> **Question:** _[example to be added]_
>
> **Generated SQL query:**
> ```sql
> [example to be added]
> ```
>
> **Result:** _[example to be added]_

## Known limitations

Some typical limitations observed during development:
- Possible model hallucinations on complex schemas or ambiguous questions
- Sensitivity to question phrasing (different queries for semantically equivalent questions)
- Dependency on the quality of the local LLM used
