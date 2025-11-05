# -*- coding: utf-8 -*-
"""
Stilometrie Analyse - Mommsen Only
Arbeitsverzeichnis: C:\Mommsen_DH\3_1_Stilometrie_Mommsen
"""

from pathlib import Path
import spacy
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. spaCy Modell laden ---
nlp = spacy.load("de_core_news_md")

# --- 2. Pfade zu den Bänden ---
base_path = Path(r"C:\Mommsen_DH\3_1_Stilometrie_Mommsen")
buecher = [base_path / f"Buch{i}" for i in range(1,6)]

# --- 3. Kapiteltexte einlesen ---
texte = {}
for i, buch in enumerate(buecher, start=1):
    for kapitel in sorted(buch.glob("kapitel_*.txt")):
        key = f"Buch{i}_{kapitel.stem}"  # z.B. Buch1_kapitel_01
        with open(kapitel, encoding="utf-8") as f:
            texte[key] = f.read()

# --- 4. Funktion zur Berechnung der Stilmetriken ---
def analyse_stil(text):
    doc = nlp(text)
    satzlaengen = [len(sent) for sent in doc.sents]
    adjektive = [token for token in doc if token.pos_ == "ADJ"]
    return {
        "durchschnittliche_satzlaenge": sum(satzlaengen)/len(satzlaengen) if satzlaengen else 0,
        "adjektivdichte": len(adjektive)/len(doc) if len(doc) > 0 else 0,
        "durchschnittliche_wortlaenge": sum(len(token) for token in doc)/len(doc) if len(doc) > 0 else 0
    }

# --- 5. Analyse für alle Kapitel ---
results = {kapitel: analyse_stil(text) for kapitel, text in texte.items()}

# --- 6. Ergebnisse in DataFrame und CSV ---
df = pd.DataFrame(results).T
df.index.name = "Kapitel"
df.to_csv(base_path / "stilometrie_mommsen.csv", encoding="utf-8")

# --- 7. Visualisierung ---
# 7a. Durchschnittliche Satzlänge pro Kapitel
plt.figure(figsize=(12,6))
plt.bar(df.index, df['durchschnittliche_satzlaenge'], color="skyblue")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Durchschnittliche Satzlänge")
plt.title("Mommsen: Satzlängen pro Kapitel")
plt.tight_layout()
plt.savefig(base_path / "satzlaenge_pro_kapitel.png")
plt.close()

# 7b. Adjektivdichte pro Kapitel
plt.figure(figsize=(12,6))
plt.bar(df.index, df['adjektivdichte'], color="salmon")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Adjektivdichte")
plt.title("Mommsen: Adjektivdichte pro Kapitel")
plt.tight_layout()
plt.savefig(base_path / "adjektivdichte_pro_kapitel.png")
plt.close()

# 7c. Durchschnittliche Wortlänge pro Kapitel
plt.figure(figsize=(12,6))
plt.bar(df.index, df['durchschnittliche_wortlaenge'], color="lightgreen")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Durchschnittliche Wortlänge")
plt.title("Mommsen: Wortlänge pro Kapitel")
plt.tight_layout()
plt.savefig(base_path / "wortlaenge_pro_kapitel.png")
plt.close()

# --- 8. Durchschnitt pro Buch berechnen ---
buch_durchschnitt = {}

for i in range(1,6):
    buch_kapitel = [k for k in df.index if k.startswith(f"Buch{i}_")]
    buch_durchschnitt[f"Buch{i}"] = df.loc[buch_kapitel].mean()

df_buch = pd.DataFrame(buch_durchschnitt).T
df_buch.index.name = "Buch"
df_buch.to_csv(base_path / "stilometrie_mommsen_pro_buch.csv", encoding="utf-8")

# --- 9. Visualisierung pro Buch ---
plt.figure(figsize=(10,6))
plt.bar(df_buch.index, df_buch['durchschnittliche_satzlaenge'], color="skyblue")
plt.ylabel("Durchschnittliche Satzlänge")
plt.title("Mommsen: Durchschnittliche Satzlänge pro Buch")
plt.savefig(base_path / "satzlaenge_pro_buch.png")
plt.close()

plt.figure(figsize=(10,6))
plt.bar(df_buch.index, df_buch['adjektivdichte'], color="salmon")
plt.ylabel("Adjektivdichte")
plt.title("Mommsen: Adjektivdichte pro Buch")
plt.savefig(base_path / "adjektivdichte_pro_buch.png")
plt.close()

plt.figure(figsize=(10,6))
plt.bar(df_buch.index, df_buch['durchschnittliche_wortlaenge'], color="lightgreen")
plt.ylabel("Durchschnittliche Wortlänge")
plt.title("Mommsen: Wortlänge pro Buch")
plt.savefig(base_path / "wortlaenge_pro_buch.png")
plt.close()

print("Durchschnitt pro Buch berechnet und Visualisierungen gespeichert.")


print("Analyse abgeschlossen. CSV und PNGs wurden gespeichert.")
