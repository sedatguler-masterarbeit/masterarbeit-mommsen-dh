import pandas as pd
import re
from pathlib import Path

# Datei Buch 5 laden
text_path = Path(r"c:\Mommsen_DH\1_3_KWIC_Helden_und_Antihelden\Buch5.txt")
text = text_path.read_text(encoding="utf-8")

# Liste der Figuren
figures = ["Caesar", "Sertorius",  "Pompeius", "Crassus", "Cicero", "Cato"]

def kwic(text, keyword, window=10):
    tokens = re.findall(r"\b\w+\b", text)
    results = []
    for i, token in enumerate(tokens):
        if token.lower() == keyword.lower():
            left = " ".join(tokens[max(0, i-window):i])
            right = " ".join(tokens[i+1:i+1+window])
            results.append((keyword, left, right))
    return results

all_kwic = []
for fig in figures:
    results = kwic(text, fig, window=10)
    for keyword, left, right in results:
        all_kwic.append({
            "Keyword": keyword,
            "LeftContext": left,
            "RightContext": right
        })

df_kwic = pd.DataFrame(all_kwic)
df_kwic.to_csv("KWIC_Helden_Buch5.csv", index=False, encoding="utf-8")

print(f"{len(df_kwic)} Treffer in Buch 5")
print(df_kwic.groupby('Keyword').size())