import pandas as pd
from pathlib import Path
import re

# Absoluter Pfad als Rohstring
data_folder = Path(r"c:\Mommsen_DH\1_2_KWIC_Senat_als_Querschnittsbegriff\Buch")

# Liste der Buch-Dateien
books = ["Buch1.txt", "Buch2.txt", "Buch3.txt", "Buch4.txt", "Buch5.txt"]

# KWIC-Funktion
def kwic(text, keyword, window=10):
    tokens = re.findall(r"\b\w+\b", text)
    results = []
    for i, token in enumerate(tokens):
        if token.lower() == keyword.lower():
            left = " ".join(tokens[max(0, i-window):i])
            right = " ".join(tokens[i+1:i+1+window])
            results.append((left, token, right))
    return results

all_kwic = []

for book in books:
    book_path = data_folder / book
    if not book_path.exists():
        print(f"Datei nicht gefunden: {book_path}")
        continue
    with open(book_path, "r", encoding="utf-8") as f:
        text = f.read()
        results = kwic(text, "Senat", window=10)
        for left, keyword, right in results:
            all_kwic.append({
                "Buch": book.replace(".txt", ""),
                "LeftContext": left,
                "Keyword": keyword,
                "RightContext": right
            })

df_kwic = pd.DataFrame(all_kwic)
output_path = data_folder / "KWIC_Senat_Buecher1-5.csv"
df_kwic.to_csv("KWIC_Senat_Buecher1-5.csv", index=False, encoding="utf-8")

print(f"Gespeichert: {len(df_kwic)} Treffer in {output_path}")
