# =======================================================
# BERTopic – Theodor Mommsen, Römische Geschichte (Buch 1–5, kapitelweise)
# Erweiterte Analyse: Statistik, Timeline, Dauerhaftigkeit
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
                "in", "ein", "wie", "nach", "im", "für", "nicht", "mit", "oder", "und", "von", "zu",
                "allein", "alles", "alle", "allerdings", "auf", "auch", "aber", "aus", "an", "als",
                "diese", "dies", "die", "dieser", "der", "das", "daß", "dem", "den", "des", "durch", "darauf",
                "er", "es", "hatte", "sich", "sein", "ist", "um", "wieder", "war", "ward", "wäre", "wären",
                "10", "20", "21"
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
    min_topic_size=80,   # reduziert kleine, irrelevante Topics
    nr_topics="auto",
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

# =======================================================
# VARIANTE B – Erweiterte Statistik / Visualisierung
# =======================================================

try:
    print("\n📊 Erstelle erweiterte Statistik und Timeline ...")

    # === DataFrame vorbereiten ===
    df = pd.DataFrame({"Document": range(len(docs)), "Topic": topics})

    # Buchzuordnung grob über Dokumentindex
    df["Book"] = df["Document"] // (len(docs) / 5) + 1
    df["Book"] = df["Book"].astype(int)

    # === Themen nach Buch zählen ===
    topic_counts = (
        df[df["Topic"] > 0]  # ignoriere -1 und 0
        .groupby(["Book", "Topic"])
        .size()
        .reset_index(name="Count")
    )

    # Nur Top 10 häufigste Topics für bessere Lesbarkeit
    top_topics = (
        topic_counts.groupby("Topic")["Count"].sum().nlargest(10).index.tolist()
    )
    topic_counts = topic_counts[topic_counts["Topic"].isin(top_topics)]

    pivot = topic_counts.pivot(index="Book", columns="Topic", values="Count").fillna(0)

    # === Legende mit Top-Wörtern ===
    topic_labels = {}
    for t in pivot.columns:
        words = [w for w, _ in topic_model.get_topic(t)[:3]]
        topic_labels[t] = f"Topic {t}: " + ", ".join(words)

    # === Grafik 1: Themenverteilung pro Buch ===
    plt.figure(figsize=(12, 6))
    colors = plt.cm.tab20.colors
    for i, topic in enumerate(pivot.columns):
        plt.plot(pivot.index, pivot[topic], marker="o", color=colors[i % len(colors)], label=topic_labels[topic])

    plt.xlabel("Buchnummer")
    plt.ylabel("Anzahl Segmente")
    plt.title("Thematische Relevanz pro Buch (Mommsen, Römische Geschichte)")
    plt.legend(
        loc="upper right",
        bbox_to_anchor=(1.4, 1),
        fontsize="x-small",
        title="Topics (Top 3 Keywords)"
    )
    plt.tight_layout()
    plt_path2 = os.path.join(output_folder, "Topic_Distribution_per_Book.png")
    plt.savefig(plt_path2)
    print(f"📈 Buchweise Themenverteilung gespeichert unter: {plt_path2}")

    # === Grafik 2: Topic-Timeline (Entwicklung über Bücher) ===
    topic_trend = (
        df[df["Topic"].isin(top_topics)]
        .groupby(["Topic", "Book"])
        .size()
        .reset_index(name="Count")
    )

    plt.figure(figsize=(12, 6))
    for topic in topic_trend["Topic"].unique():
        subset = topic_trend[topic_trend["Topic"] == topic]
        plt.plot(subset["Book"], subset["Count"], marker="o", color=colors[topic % len(colors)], label=topic_labels[topic])

    plt.xlabel("Buchnummer")
    plt.ylabel("Vorkommen (Segmente)")
    plt.title("Themenverlauf über die Bücher (Topic Timeline)")
    plt.legend(bbox_to_anchor=(1.4, 1), loc="upper right", fontsize="x-small", title="Topics")
    plt.tight_layout()
    timeline_path = os.path.join(output_folder, "Topic_Timeline.png")
    plt.savefig(timeline_path)
    print(f"📉 Themenverlauf gespeichert unter: {timeline_path}")

    # === Dauerhafte vs. temporäre Themen ===
    topic_presence = (
        df[df["Topic"] > 0]
        .groupby("Topic")["Book"]
        .nunique()
        .reset_index(name="BookCount")
    )

    persistent_topics = topic_presence[topic_presence["BookCount"] == 5]["Topic"].tolist()
    temporary_topics = topic_presence[topic_presence["BookCount"] < 3]["Topic"].tolist()

    print("\n📘 Dauerhafte Themen (in allen 5 Büchern vertreten):", persistent_topics)
    print("📕 Temporäre Themen (nur in 1–2 Büchern):", temporary_topics)

except Exception as e:
    print(f"⚠️ Fehler in der erweiterten Statistik: {e}")

print("\n✅ Fertig! Topic-Modelling und erweiterte Visualisierungen abgeschlossen.")
