import pandas as pd
import spacy
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# === 1. CSV laden (tab-getrennt!) ===
file_path = "KWIC_Senat_Buecher1_5_process.csv"
df = pd.read_csv(file_path, sep="\t", engine="python")

# === 2. Spalten prüfen und vereinheitlichen ===
print("Erkannte Originalspalten:", df.columns.tolist())

# Spaltennamen aufräumen
df.columns = [c.strip().lower().replace(" ", "").replace("\t", "") for c in df.columns]
print("Bereinigte Spalten:", df.columns.tolist())

# Automatisches Mapping
try:
    left_col = [c for c in df.columns if "left" in c][0]
    right_col = [c for c in df.columns if "right" in c][0]
    keyword_col = [c for c in df.columns if "key" in c][0]
    buch_col = [c for c in df.columns if "buch" in c or "band" in c][0]
except IndexError:
    raise ValueError("Fehler: Bitte prüfe die Spaltennamen in deiner TSV-Datei.")

df = df.rename(columns={
    buch_col: 'band',
    left_col: 'left',
    right_col: 'right',
    keyword_col: 'keyword'
})

print("\nSpalten nach Umbenennung:", df.columns.tolist())

# === 3. Kontext vorbereiten ===
df['context'] = df['left'].astype(str) + " " + df['keyword'].astype(str) + " " + df['right'].astype(str)


# === 4. Sprachmodell laden ===
# Wenn dein Text lateinisch ist, verwende statt de_core_news_md: spacy.load("xx_ent_wiki_sm")
nlp = spacy.load("de_core_news_md")

# === 5. Adjektive extrahieren ===
def extract_adjectives(text):
    doc = nlp(text)
    return [token.lemma_.lower() for token in doc if token.pos_ == "ADJ"]

print("\nAdjektive werden extrahiert – kann bei 800 Zeilen ein paar Minuten dauern ...")
df['adjectives'] = df['context'].apply(extract_adjectives)

# === 6. Adjektivhäufigkeiten pro Band berechnen ===
adj_counts_per_band = {}
for band, group in df.groupby('band'):
    all_adj = [adj for lst in group['adjectives'] for adj in lst]
    counts = Counter(all_adj)
    adj_counts_per_band[band] = counts

# === 7. DataFrame für Heatmap erstellen ===
# 20 häufigste Adjektive insgesamt
all_adjs = Counter()
for c in adj_counts_per_band.values():
    all_adjs.update(c)
top_adjs = [w for w, _ in all_adjs.most_common(20)]

heatmap_data = pd.DataFrame(index=top_adjs)

for band, counts in adj_counts_per_band.items():
    freq_dict = {adj: counts[adj] for adj in top_adjs}
    heatmap_data[band] = pd.Series(freq_dict)

heatmap_data = heatmap_data.fillna(0)

# === 8. Heatmap zeichnen ===
plt.figure(figsize=(10, 8))
sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt=".0f")
plt.title("Adjektivverteilung im Umfeld von 'Senat' – pro Buch")
plt.xlabel("Buch")
plt.ylabel("Adjektive")
plt.tight_layout()
plt.show()

# === 9. Optional: Wordclouds pro Buch ===
for band, counts in adj_counts_per_band.items():
    wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(counts)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.title(f"Adjektive im Umfeld von 'Senat' – Buch {band}")
    plt.show()

# === 10. Ergebnisse exportieren ===
heatmap_data.to_csv("KWIC_Senat_Adjektive_Heatmap.csv", encoding='utf-8')
df.to_csv("KWIC_Senat_Adjektive_pro_Buch.csv", index=False, encoding='utf-8')

print("\nFertig ✅ – Dateien wurden gespeichert.")
