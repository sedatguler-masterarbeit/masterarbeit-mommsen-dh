# ==========================================
# Mommsen – Sentimentanalyse zur römischen Bevölkerung
# ==========================================
# Voraussetzungen:
# pip install transformers pandas matplotlib nltk tqdm torch
# ==========================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline
from tqdm import tqdm
import nltk
from nltk.tokenize import sent_tokenize

# NLTK-Resourcen
nltk.download("punkt")
nltk.download("punkt_tab")

# ==========================================
# 1️⃣ Pfad anpassen
# ==========================================
base_folder = Path("C:/Mommsen_DH/2_1_Sentimentanalyse_BERT") 

# ==========================================
# 2️⃣ Suchbegriffe definieren (stichwortartig)
# ==========================================
keywords = [
    "Volk", "Volks", "Bevölkerung", "Bürger", "Bürgerschaft", "Stadtbevölkerung",
    "römische Bevölkerung", "römisches Volk", "römischen Volk",
    "Plebs", "Pöbel", "Menge", "Mob", "Proletarier", "Volkshaufen"
]

# ==========================================
# 3️⃣ Bücher & Kapitel rekursiv einlesen
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
# 4️⃣ Filterung auf Passagen mit relevanten Begriffen
# ==========================================
def contains_keywords(text, keywords):
    for kw in keywords:
        if kw.lower() in text.lower():
            return True
    return False

df_filtered = df[df["text"].apply(lambda x: contains_keywords(x, keywords))]
print(f"📊 Gefundene Kapitel mit relevanten Begriffen: {len(df_filtered)}")

# ==========================================
# 5️⃣ BERT-Sentimentmodell laden
# ==========================================
print("🔍 Lade BERT-Sentimentmodell ...")
sentiment_model = pipeline("sentiment-analysis", model="oliverguhr/german-sentiment-bert")

# ==========================================
# 6️⃣ Sentimentanalyse pro Kapitel (nur relevante Kapitel)
# ==========================================
results = []

for _, row in tqdm(df_filtered.iterrows(), total=len(df_filtered), desc="Analysiere Kapitel"):
    text = row["text"]
    sentences = sent_tokenize(text)
    # Nur Sätze, in denen eines der Keywords vorkommt
    sentences_relevant = [s for s in sentences if any(kw.lower() in s.lower() for kw in keywords)]
    if not sentences_relevant:
        continue

    sentiments = sentiment_model(sentences_relevant)
    score_sum = 0
    for s in sentiments:
        if s["label"] == "positive":
            score_sum += s["score"]
        elif s["label"] == "negative":
            score_sum -= s["score"]
    avg_score = score_sum / len(sentiments)

    results.append({
        "book": row["book"],
        "chapter": row["chapter"],
        "num_sentences": len(sentences_relevant),
        "sentiment_score": avg_score
    })

sent_df = pd.DataFrame(results)
sent_df.to_csv("Mommsen_Sentiment_Bevoelkerung.csv", index=False, encoding="utf-8-sig")
print("💾 Ergebnisse gespeichert unter: Mommsen_Sentiment_Bevoelkerung.csv")

# ==========================================
# 7️⃣ Aggregation nach Buch
# ==========================================
sentiment_by_book = sent_df.groupby("book")["sentiment_score"].mean().reset_index()

# ==========================================
# 8️⃣ Visualisierung
# ==========================================
plt.figure(figsize=(8,5))
plt.plot(sentiment_by_book["book"], sentiment_by_book["sentiment_score"], marker="o", linewidth=2, color="darkred")
plt.title("Tonalität der Darstellung der römischen Bevölkerung bei Mommsen")
plt.xlabel("Buch")
plt.ylabel("Durchschnittliches Sentiment (nur Passagen zur Bevölkerung)")
plt.grid(True)
plt.tight_layout()
plt.savefig("Mommsen_Sentiment_Bevoelkerung.png", dpi=300)
plt.show()

print("✅ Analyse abgeschlossen.")
