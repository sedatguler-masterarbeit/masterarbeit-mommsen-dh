import os
import re
import spacy
from collections import Counter

# -----------------------------
# CONFIGURATION
# -----------------------------

# Verzeichnis mit den Kapiteln
INPUT_DIR = r"C:/Mommsen_DH/Judentum/KWIC/Buch8_Kap10_11"

# Liste der jüdischen Schlüsselbegriffe (Case-insensitive)
KEYWORDS = [
    "jude", "juden", "jüdisch", "judäa", "jerusalem",
    "israeliten", "herodes", "diaspora"
]

# KWIC-Fenstergröße
WINDOW = 10   # Anzahl Wörter links/rechts


# -----------------------------
# LOAD SPACY MODEL
# -----------------------------
print("Lade spaCy Modell (de_core_news_md)...")
try:
    nlp = spacy.load("de_core_news_md")
except:
    print("Modell fehlt. Installiere mit:")
    print("python -m spacy download de_core_news_md")
    raise


# -----------------------------
# HELFER: KWIC FUNKTION
# -----------------------------
def kwic(text, keyword, window=6):
    """Return list of (left, keyword, right) windows."""
    tokens = text.split()
    results = []

    for i, tok in enumerate(tokens):
        if keyword.lower() in tok.lower():     # fuzzy match
            left = " ".join(tokens[max(0, i-window):i])
            right = " ".join(tokens[i+1:i+1+window])
            results.append((left, tok, right))
    return results


# -----------------------------
# HAUPTPROGRAMM
# -----------------------------
all_kwic_results = []
all_adj = []

print("\n--- Starte Analyse ---\n")

for fname in os.listdir(INPUT_DIR):
    if not fname.endswith(".txt"):
        continue

    path = os.path.join(INPUT_DIR, fname)
    print(f"Verarbeite Datei: {fname}")

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # KWIC pro Keyword
    for kw in KEYWORDS:
        hits = kwic(text, kw, WINDOW)
        for left, word, right in hits:
            full_window = f"{left} {word} {right}"
            all_kwic_results.append((fname, kw, left, word, right))

            # spaCy Analyse des Kontextfensters
            doc = nlp(full_window)

            # Adjektive extrahieren
            for token in doc:
                if token.pos_ == "ADJ":
                    lemma = token.lemma_.lower()
                    all_adj.append(lemma)


# -----------------------------
# AUSWERTUNG
# -----------------------------

adj_freq = Counter(all_adj)

print("\n\n=======================")
print("  KWIC: Trefferliste")
print("=======================")

for fname, kw, left, word, right in all_kwic_results[:40]:
    print(f"[{fname}] {left} >>> {word} <<< {right}")

print("\n(Es werden nur die ersten 40 Beispiele angezeigt.)")


print("\n\n=======================")
print("  HÄUFIGSTE ADJEKTIVE IM KWIC-UMFELD")
print("=======================")

for adj, count in adj_freq.most_common(30):
    print(f"{adj:20} {count}")


# -----------------------------
# OPTIONAL: CSV EXPORT
# -----------------------------
import csv

csv_path = os.path.join(INPUT_DIR, "KWIC_Judentum_Mommsen.csv")
adj_csv_path = os.path.join(INPUT_DIR, "Adjektive_Judentum_Mommsen.csv")

with open(csv_path, "w", encoding="utf-8", newline="") as out:
    writer = csv.writer(out)
    writer.writerow(["datei", "keyword", "left", "word", "right"])
    writer.writerows(all_kwic_results)

with open(adj_csv_path, "w", encoding="utf-8", newline="") as out:
    writer = csv.writer(out)
    writer.writerow(["adjektiv", "freq"])
    for adj, freq in adj_freq.items():
        writer.writerow([adj, freq])

print("\nCSV-Dateien gespeichert:")
print(" →", csv_path)
print(" →", adj_csv_path)

print("\nAnalyse abgeschlossen.")
