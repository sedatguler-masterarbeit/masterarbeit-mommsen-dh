import os
import re
from collections import Counter

# Liste der Begriffe (in Kleinbuchstaben für matching)
terms = [
    "jude", "juden", "jüdisch", "judäa", "israeliten",
    "jerusalem", "herodes", "pharisäer", "sadduzäer",
    "zeloten", "makkabäer", 
    "diaspora", "jahwe", "juda", "jüdische", "gemeinde",
    "Pharisäer", "Sadduzäer", "Zeloten", "Makkabäer",
    "Diaspora", "Jahwe", "Juda", "Jüdinnen", "Jüdische Gemeinde"
]

# Pfad zum Ordner mit den Büchern
base_path = "C:/Mommsen_DH/Judentum/1_Frequenzanalyse/Buch"

# Ausgabe-Datenstruktur: Buchnummer -> Counter
freq_by_book = {}

# Funktion: Text normalisieren (Klein, Wortgrenzen)
def tokenize(text):
    # einfache Tokenisierung: nur Wortzeichen
    return re.findall(r"\w+", text.lower())

for book_num in [1,2,3,4,5,8]:
    folder = f"{base_path}{book_num}"
    if not os.path.isdir(folder):
        print(f"Warnung: Ordner nicht gefunden: {folder}")
        continue

    book_counter = Counter()
    total_tokens = 0

    # alle .txt-Dateien im Ordner durchlaufen
    for fname in os.listdir(folder):
        if not fname.lower().endswith(".txt"):
            continue
        path = os.path.join(folder, fname)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        tokens = tokenize(text)
        total_tokens += len(tokens)

        # Begriffe zählen
        for term in terms:
            book_counter[term] += tokens.count(term)

    freq_by_book[book_num] = {
        "counts": book_counter,
        "total_tokens": total_tokens
    }

# Ausgabe
print("Frequenzanalyse jüdischer Begriffe pro Buch:")
for book_num, data in freq_by_book.items():
    print(f"\nBuch {book_num}:")
    counts = data["counts"]
    total = data["total_tokens"]
    for term in terms:
        cnt = counts[term]
        rel = cnt / total if total > 0 else 0
        print(f"  {term}: {cnt} ({rel:.6f} Anteil)")

# Optional: Speichern als Datei
out_path = "C:/Mommsen_DH/Judentum/frequenz_judentum.csv"
with open(out_path, "w", encoding="utf-8") as out:
    out.write("Buch,Term,Count,Relative\n")
    for book_num, data in freq_by_book.items():
        total = data["total_tokens"]
        for term in terms:
            cnt = data["counts"][term]
            rel = cnt / total if total > 0 else 0
            out.write(f"{book_num},{term},{cnt},{rel:.8f}\n")
print(f"\nErgebnisse gespeichert in {out_path}")
