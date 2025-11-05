import pandas as pd
import spacy
from collections import Counter
from pathlib import Path

# === Parameter ===
data_file = Path(r"C:\Mommsen_DH\1_3a_KWIC_Helden_und_Antihelden_Analyse\KWIC_Helden_Buch5_process.csv")
output_folder = Path(r"C:\Mommsen_DH\1_3a_KWIC_Helden_und_Antihelden_Analyse\Results")
output_folder.mkdir(exist_ok=True)  # Ordner erstellen, falls nicht vorhanden
figures = ["Caesar", "Sertorius", "Pompeius", "Crassus", "Cato", "Cicero"]

# === Sprachmodell laden ===
nlp = spacy.load("de_core_news_lg")

# === CSV einlesen ===
df = pd.read_csv(data_file, sep="\t", engine='python')  # Tab-getrennt

# === Spalten bereinigen: Leerzeichen entfernen ===
df.columns = [c.strip() for c in df.columns]

# === Prüfen, ob die erwarteten Spalten existieren ===
expected_cols = ["LeftContext", "Keyword", "RightContext"]
for col in expected_cols:
    if col not in df.columns:
        raise ValueError(f"Spalte '{col}' nicht gefunden. Verfügbare Spalten: {df.columns.tolist()}")

# === Textkontext zusammenführen ===
df["context"] = df["LeftContext"].astype(str) + " " + df["Keyword"].astype(str) + " " + df["RightContext"].astype(str)

# === Positiv/Negativ-Wörterbuch (Beispiele, erweiterbar) ===
positive_words = set([
    "tapfer", "klug", "weise", "gerecht", "ehrenhaft", "heldenhaft", "mutig", "ruhmbegierig", "erfolgreich", "tugendhaft",
    "siegt", "führt", "verteidigt", "opfert", "bewundert",
    # SG
    "vorzüglich", "talentiert", "glücklich", "zuverlässig", "genie",
    "gut", "bestimmt", "würdevoll", "gebildet", "stark"    
])

negative_words = set([
    "feige", "schwach", "korrupt", "ehrgeizig", "verdorben", "tyrannisch", "listig", "neidisch", "unterliegt", "scheitert",
    "verrät", "unterdrückt", "missachtet",
    # SG
    "eifersüchtig", "ärgerlich", "schändlich", "achselträger",
    "albern"    
])

# === Ergebnisse speichern ===
results = {}

for name in figures:
    subset = df[df["Keyword"].str.contains(name, case=False, na=False)]
    if subset.empty:
        print(f"Warnung: Keine Treffer für {name}")
        continue

    texts = " ".join(subset["context"].tolist())
    doc = nlp(texts)

    adjectives = [token.lemma_ for token in doc if token.pos_ == "ADJ" and len(token.text) > 2]
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB" and len(token.text) > 2]
    nouns = [token.lemma_ for token in doc if token.pos_ == "NOUN" and len(token.text) > 2]

    # --- positive/negative Zählung ---
    pos_count = sum(1 for w in adjectives+verbs+nouns if w in positive_words)
    neg_count = sum(1 for w in adjectives+verbs+nouns if w in negative_words)

    results[name] = {
        "Top_Adjektive": Counter(adjectives).most_common(15),
        "Top_Verben": Counter(verbs).most_common(15),
        "Top_Substantive": Counter(nouns).most_common(15),
        "Positive_Words": pos_count,
        "Negative_Words": neg_count
    }

# === Ausgabe ===
for name, data in results.items():
    print(f"\n=== {name} ===")
    print("Adjektive:", data["Top_Adjektive"])
    print("Verben:", data["Top_Verben"])
    print("Substantive:", data["Top_Substantive"])
    print("Positiv konnotierte Wörter:", data["Positive_Words"])
    print("Negativ konnotierte Wörter:", data["Negative_Words"])

    # === Textdatei schreiben ===
    output_file = output_folder / f"{name}_results.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"=== {name} ===\n\n")
        f.write("Top Adjektive:\n")
        for adj, count in Counter(adjectives).most_common(15):
            f.write(f"{adj}: {count}\n")
        f.write("\nTop Verben:\n")
        for verb, count in Counter(verbs).most_common(15):
            f.write(f"{verb}: {count}\n")
        f.write("\nTop Substantive:\n")
        for noun, count in Counter(nouns).most_common(15):
            f.write(f"{noun}: {count}\n")
        f.write(f"\nPositiv konnotierte Wörter: {pos_count}\n")
        f.write(f"Negativ konnotierte Wörter: {neg_count}\n")

    print(f"Ergebnisse für {name} gespeichert: {output_file}")
