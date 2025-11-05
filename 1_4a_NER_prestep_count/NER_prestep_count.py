from pathlib import Path
import spacy
import pandas as pd

# === Pfade ===
data_folder = Path("c:/Mommsen_DH/1_4a_NER_prestep_count/Buch")
output_file = Path("c:/Mommsen_DH/1_4a_NER_prestep_count/NER_Counts_per_Book.csv")

# === Sprachmodell ===
nlp = spacy.load("de_core_news_lg")

# === Hilfsfunktion: Text in Blöcke teilen ===
def split_text(text, max_length=80000):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

# === Ergebnisse ===
results = []

for book_path in sorted(data_folder.glob("Buch*.txt")):
    book_name = book_path.stem
    print(f"Verarbeite {book_name}...")

    text = book_path.read_text(encoding="utf-8")
    chunks = split_text(text)

    person_count = 0
    loc_count = 0
    org_count = 0

    for i, chunk in enumerate(chunks):
        doc = nlp(chunk)
        person_count += sum(1 for ent in doc.ents if ent.label_ == "PER")
        loc_count += sum(1 for ent in doc.ents if ent.label_ in ["LOC", "GPE"])
        org_count += sum(1 for ent in doc.ents if ent.label_ == "ORG")
        print(f"  Chunk {i+1}/{len(chunks)} verarbeitet")

    results.append({
        "Buch": book_name,
        "Personen": person_count,
        "Orte": loc_count,
        "Institutionen": org_count
    })

# === CSV-Ausgabe ===
df = pd.DataFrame(results)
df.to_csv(output_file, index=False, encoding="utf-8")

print("\nFertig! Ergebnisse gespeichert unter:")
print(output_file)
print(df)
