# =======================================================
# BERTopic – Theodor Mommsen, Römische Geschichte (Buch 1–5, kapitelweise)
# =======================================================

from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import os
import pandas as pd
import matplotlib.pyplot as plt

# === Pfade ===
input_folder = r"C:\Mommsen_DH\2_2_Topicmodelling_BERTopic"
output_folder = r"C:\Mommsen_DH\2_2_Topicmodelling_BERTopic"
os.makedirs(output_folder, exist_ok=True)

# === Alle fünf Bücher kapitelweise laden ===
docs = []

for i in range(1, 6):
    book_folder = os.path.join(input_folder, f"Buch{i}")
    if not os.path.isdir(book_folder):
        print(f"⚠️ Ordner nicht gefunden: {book_folder}")
        continue

    chapter_files = sorted([f for f in os.listdir(book_folder) if f.endswith(".txt")])
    print(f"📗 Buch {i}: {len(chapter_files)} Kapitel gefunden")

    for chapter in chapter_files:
        path = os.path.join(book_folder, chapter)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

            # Segmentiere Text grob in Absätze / Sätze
            segments = [t.strip() for t in text.split(".") if len(t.strip()) > 30]

            # === Manuelle Stopwords ===
            custom_stopwords = {
                "in",  "ein", "wie", "10", "20", "21", "nach", "im", "für", "gewesen",   "nicht",  "nachher",  "mit", "oder",
                
                 #
                "allein", "alles", "alle", "allerdings", "auf", "auch", "aber", "aus", "an", "als",
                "bald",
                "diese", "dies", "die", "dieser", "der", "das", "daß", "dem", "den", "des", "durch", "darauf",
                "er",  "es", 
                "hatte",

                "sich", "sein", "ist",
                "um", "und",
                "von",
                "wieder", "war", "ward", "wäre", "wären",                

                "zu"
            }

            segments = [
                " ".join([w for w in t.split() if w not in custom_stopwords])
                for t in segments
            ]
            # === /manuelle Stopwords ===

            docs.extend(segments)
            print(f"  📄 {chapter}: {len(segments)} Segmente geladen")

print(f"\n✅ Insgesamt {len(docs)} Textsegmente aus 5 Büchern (kapitelweise) geladen.\n")

# === SentenceTransformer-Embeddingmodell laden ===
print("🔍 Lade SentenceTransformer (all-MiniLM-L6-v2)...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# === BERTopic-Modell initialisieren ===
topic_model = BERTopic(
    embedding_model=embedding_model,
    top_n_words=10,
    min_topic_size=100,  # SG bisher: 10 → teste Werte 30–100     ---- kleiner, verwandte Topics zusammenführen
    nr_topics="auto",  # SG reduzieren auf ~25 Hauptthemen
    verbose=True
)

# === Topic-Modelling durchführen ===
print("🚀 Führe Topic-Modelling durch ...")
topics, probs = topic_model.fit_transform(docs)

# === Themenübersicht ===
topic_info = topic_model.get_topic_info()
print("\n📊 Themenübersicht:")
print(topic_info.head(10))

# === Ergebnisse speichern ===
topic_info_path = os.path.join(output_folder, "topic_info_all_books.csv")
topic_info.to_csv(topic_info_path, index=False, encoding="utf-8")
print(f"\n💾 Themenübersicht gespeichert unter: {topic_info_path}")

# === Top-Wörter der wichtigsten Themen ===
for topic_num in topic_info["Topic"].head(5):
    if topic_num != -1:
        print(f"\n🧩 Thema {topic_num}:")
        print(topic_model.get_topic(topic_num))

# === Modell speichern ===
model_path = os.path.join(output_folder, "Mommsen_BERTopic_Model_All")
topic_model.save(model_path)
print(f"\n💾 Modell gespeichert unter: {model_path}")

# === Interaktive Visualisierung ===
try:
    print("📈 Erstelle interaktive Visualisierung (HTML)...")
    fig = topic_model.visualize_topics()
    html_path = os.path.join(output_folder, "Mommsen_BERTopic_Topics_All.html")
    fig.write_html(html_path)
    print(f"✅ Interaktive Visualisierung gespeichert unter: {html_path}")
except Exception as e:
    print(f"⚠️ Visualisierung konnte nicht erstellt werden: {e}")

# === Statistische Verteilung ===
try:
    topic_freq = topic_info[topic_info["Topic"] >= 0]
    plt.bar(topic_freq["Topic"], topic_freq["Count"])
    plt.xlabel("Topic Nummer")
    plt.ylabel("Dokumentenanzahl")
    plt.title("Verteilung der Themen (Mommsen, alle Bücher)")
    plt.tight_layout()
    plt_path = os.path.join(output_folder, "Topic_Distribution_All.png")
    plt.savefig(plt_path)
    print(f"📊 Diagramm gespeichert unter: {plt_path}")
except Exception as e:
    print(f"⚠️ Kein Diagramm erstellt: {e}")

print("\n✅ Fertig! Topic-Modelling für alle fünf Bände abgeschlossen.")
