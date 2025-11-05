# --- Mommsen Buch 5: Figurenanalyse mit multilingualem BERT-Sentiment ---
# Modell: nlptown/bert-base-multilingual-uncased-sentiment
# Skala: 1 = sehr negativ, 5 = sehr positiv → Umrechnung auf -1 bis +1

from transformers import pipeline
from nltk.tokenize import sent_tokenize
import nltk
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# --- Setup ---
nltk.download('punkt')
nltk.download('punkt_tab')

# --- Pfade ---
path = Path(r"C:\Mommsen_DH\2_1_Sentimentanalyse_BERT\Buch5")
output_folder = path

# --- Modell laden ---
sentiment_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# --- Figuren definieren ---
figuren = {
    "Caesar": ["Caesar"],
    "Sertorius": ["Sertorius"],
    "Pompeius": ["Pompeius"],
    "Crassus": ["Crassus"],
    "Cato": ["Cato"],
    "Cicero": ["Cicero"]
}

window = 2  # Sätze um jede Nennung
results = []

# --- Alle Kapiteldateien verarbeiten ---
for file in sorted(path.glob("Kapitel_*.txt")):
    kapitelname = file.stem
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    sentences = sent_tokenize(text)

    for name, aliases in figuren.items():
        indices = [i for i, s in enumerate(sentences) if any(a in s for a in aliases)]
        for idx in indices:
            start = max(0, idx - window)
            end = min(len(sentences), idx + window + 1)
            context = " ".join(sentences[start:end]).strip()
            if len(context) < 50:
                continue
            try:
                sentiment = sentiment_model(context[:512])[0]
                label = sentiment["label"]  # "1 star", "2 stars", ..., "5 stars"
                stars = int(label.split()[0])
                # Umrechnung auf Skala -1 (negativ) bis +1 (positiv)
                val = np.interp(stars, [1, 5], [-1, 1])
                results.append({
                    "Kapitel": kapitelname,
                    "Name": name,
                    "Sentiment": val
                })
            except Exception as e:
                print(f"Fehler bei {kapitelname}, {name}: {e}")

# --- DataFrame ---
df = pd.DataFrame(results)
if df.empty:
    raise ValueError("Keine Ergebnisse – bitte Pfad oder Text prüfen!")

# --- Aggregation ---
summary = (
    df.groupby("Name")["Sentiment"]
    .agg(["count", "mean", "min", "max"])
    .reset_index()
    .rename(columns={"count": "Anzahl Kontexte", "mean": "Ø Sentiment"})
    .round(3)
)

kapitel_summary = (
    df.groupby(["Kapitel", "Name"])["Sentiment"]
    .mean()
    .reset_index()
    .pivot(index="Kapitel", columns="Name", values="Sentiment")
    .round(3)
)

# --- CSV speichern ---
df.to_csv(output_folder / "Sentiment_Figuren_Buch5_detailliert_multilingual.csv", index=False, encoding="utf-8-sig")
summary.to_csv(output_folder / "Sentiment_Figuren_Buch5_gesamt_multilingual.csv", index=False, encoding="utf-8-sig")
kapitel_summary.to_csv(output_folder / "Sentiment_Figuren_Buch5_kapitelweise_multilingual.csv", encoding="utf-8-sig")

# --- Diagramm 1: Gesamtübersicht ---
plt.figure(figsize=(8, 5))
plt.bar(summary["Name"], summary["Ø Sentiment"], color="goldenrod")
plt.axhline(0, color="black", linewidth=0.8)
plt.title("Mommsens Figurenbewertung in Buch 5 (multilingual BERT)")
plt.ylabel("Durchschnittlicher Sentimentwert (-1 = negativ, +1 = positiv)")
plt.tight_layout()
plt.savefig(output_folder / "Sentiment_Figuren_Buch5_Gesamt_multilingual.png", dpi=300)
plt.close()

# --- Diagramm 2: Kapitelverlauf ---
plt.figure(figsize=(10, 6))
for col in kapitel_summary.columns:
    plt.plot(kapitel_summary.index, kapitel_summary[col], marker="o", label=col)
plt.axhline(0, color="black", linewidth=0.8)
plt.title("Tonalität der Figuren in Buch 5 (multilingual BERT, kapitelweise)")
plt.xlabel("Kapitel")
plt.ylabel("Ø Sentiment")
plt.legend()
plt.tight_layout()
plt.savefig(output_folder / "Sentiment_Figuren_Buch5_Kapitelverlauf_multilingual.png", dpi=300)
plt.close()

print("\n--- Fertig ---")
print(summary)
print("\nErgebnisse und PNG-Dateien gespeichert in:")
print(output_folder)

