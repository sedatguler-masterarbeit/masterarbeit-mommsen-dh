# ==========================================
# BERT-Sentimentanalyse für Mommsens Römische Geschichte
# ==========================================
# Voraussetzungen:
# pip install transformers pandas matplotlib nltk torch
# (optional: pip install tqdm für Fortschrittsbalken)
# ==========================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline
from tqdm import tqdm
import nltk

# Satzsegmentierung (nützlich, falls du Text später auf Satzebene analysieren willst)
nltk.download("punkt")
nltk.download("punkt_tab")
from nltk.tokenize import sent_tokenize

# ==========================================
# 1️⃣ Grundpfad
# ==========================================
base_folder = Path("C:/Mommsen_DH/2_1_Sentimentanalyse_BERT")

# ==========================================
# 2️⃣ Kapitel rekursiv einlesen
# ==========================================
data = []

for book_folder in sorted(base_folder.glob("Buch*")):
    book_name = book_folder.name
    print(f"📘 Lade Kapitel aus {book_name} ...")
    for chapter_file in sorted(book_folder.glob("kapitel_*.txt")):
        text = chapter_file.read_text(encoding="utf-8").strip()
        if len(text) > 0:
            data.append({
                "book": book_name,
                "chapter": chapter_file.stem,
                "text": text
            })

df = pd.DataFrame(data)
print(f"✅ Eingelesene Kapitel: {len(df)}")

# ==========================================
# 3️⃣ BERT-Sentimentmodell laden
# ==========================================
print("🔍 Lade BERT-Sentimentmodell ...")
sentiment_model = pipeline("sentiment-analysis", model="oliverguhr/german-sentiment-bert")

# ==========================================
# 4️⃣ Sentimentberechnung pro Kapitel
# ==========================================
results = []

for _, row in tqdm(df.iterrows(), total=len(df), desc="Analysiere Kapitel"):
    text = row["text"]
    # Optional: lange Kapitel in Sätze aufteilen
    sentences = sent_tokenize(text)
    sentiments = sentiment_model(sentences)

    # Durchschnittliche Bewertung über alle Sätze eines Kapitels
    score_sum = 0
    for s in sentiments:
        score = s["score"] if s["label"] == "positive" else -s["score"] if s["label"] == "negative" else 0
        score_sum += score
    avg_score = score_sum / len(sentiments)

    results.append({
        "book": row["book"],
        "chapter": row["chapter"],
        "sentiment_score": avg_score,
        "num_sentences": len(sentences)
    })

sent_df = pd.DataFrame(results)
sent_df.to_csv("Mommsen_Sentiment_pro_Kapitel.csv", index=False, encoding="utf-8-sig")
print("💾 Ergebnisse gespeichert unter: Mommsen_Sentiment_pro_Kapitel.csv")

# ==========================================
# 5️⃣ Aggregation pro Buch
# ==========================================
sentiment_by_book = sent_df.groupby("book")["sentiment_score"].mean().reset_index()

# ==========================================
# 6️⃣ Visualisierung
# ==========================================
plt.figure(figsize=(8,5))
plt.plot(sentiment_by_book["book"], sentiment_by_book["sentiment_score"], marker="o", linewidth=2)
plt.title("Gesamttonalität pro Buch (Mommsen, Römische Geschichte)")
plt.xlabel("Buch")
plt.ylabel("Durchschnittliches Sentiment")
plt.grid(True)
plt.tight_layout()
plt.savefig("Mommsen_Sentiment_pro_Buch.png", dpi=300)
plt.show()

# ==========================================
# 7️⃣ Sentimentverlauf pro Kapitel innerhalb jedes Buches
# ==========================================
plt.figure(figsize=(10,6))
for book, group in sent_df.groupby("book"):
    plt.plot(group["chapter"], group["sentiment_score"], marker=".", label=book)

plt.title("Sentimentverlauf pro Kapitel")
plt.xlabel("Kapitel")
plt.ylabel("Durchschnittliches Sentiment")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("Mommsen_Sentiment_pro_Kapitel.png", dpi=300)
plt.show()

print("✅ Analyse abgeschlossen.")

