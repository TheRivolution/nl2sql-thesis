import matplotlib.pyplot as plt
import numpy as np

# I tuoi dati reali aggiornati con i token in input veri
test_labels = ['Test 1\n(Semplice)', 'Test 2\n(Attacco)', 'Test 3\n(Calcoli)', 'Test 4\n(Err. Join)', 'Test 5\n(HAVING)', 'Test 6\n(Volumi)']
tempi = [16.28, 63.61, 38.84, 53.44, 37.66, 30.95]
token_in = [685, 693, 715, 690, 697, 718]  # I tuoi dati reali di input!
token_out = [23, 170, 95, 60, 103, 82]

# Colori per il grafico dei tempi
colori_tempi = ['#2ca02c', '#d62728', '#2ca02c', '#ff7f0e', '#2ca02c', '#2ca02c']

# --- GRAFICO 1: TEMPI DI LATENZA ---
plt.figure(figsize=(11, 6))
bars = plt.bar(test_labels, tempi, color=colori_tempi, edgecolor='black', width=0.6)
plt.title('Tempi di latenza end-to-end per scenario di test', fontsize=14, fontweight='bold')
plt.ylabel('Secondi (s)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval}s', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(r"C:\Users\Andrea\Desktop\Tirocinio\grafico_tempi.png", dpi=300)
plt.close()


# --- GRAFICO 2: CONFRONTO TOKEN (INPUT VS OUTPUT) ---
x = np.arange(len(test_labels))  # Posizioni delle etichette
width = 0.35  # Larghezza delle barre

plt.figure(figsize=(11, 6))
# Barre per i Token in Input
rects1 = plt.bar(x - width/2, token_in, width, label='Token in Input (Contesto + Domanda)', color='#1f77b4', edgecolor='black')
# Barre per i Token in Output
rects2 = plt.bar(x + width/2, token_out, width, label='Token in Output (Risposta LLM)', color='#aec7e8', edgecolor='black')

plt.title('Analisi del consumo di Token: Input vs Output', fontsize=14, fontweight='bold')
plt.ylabel('Numero di Token', fontsize=12)
plt.xticks(x, test_labels)
plt.legend(fontsize=11, loc='upper right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Aggiungo i numeri sopra le barre di Input
for rect in rects1:
    h = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2, h + 10, f'{h}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# Aggiungo i numeri sopra le barre di Output
for rect in rects2:
    h = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2, h + 10, f'{h}', ha='center', va='bottom', fontsize=9)

# Imposto il limite massimo dell'asse Y un po' più alto per non far tagliare i testi
plt.ylim(0, 850)

plt.tight_layout()
plt.savefig(r"C:\Users\Andrea\Desktop\Tirocinio\grafico_token.png", dpi=300)
plt.close()

print("Grafici aggiornati creati con successo nella cartella Tirocinio!")