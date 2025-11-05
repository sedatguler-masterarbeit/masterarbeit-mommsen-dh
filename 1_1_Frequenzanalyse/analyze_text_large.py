#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyze_text_large.py – Lemmatisierte Wortfrequenzanalyse für sehr große Texte (>1 Mio Zeichen)

Benutzung:
  python analyze_text_large.py <input.txt> [--top 50]
"""

import sys, csv
from pathlib import Path
from collections import Counter

# ======== KONFIGURATION ========

CUSTOM_MAP = {
    "caesars": "caesar", "caesarem": "caesar", "caesari": "caesar",
    "caesare": "caesar", "cæsar": "caesar", "cæsars": "caesar",
    "pompeji": "pompeius", "pompeius'": "pompeius", "pompeii": "pompeius",
    "ciceronis": "cicero", "ciceronem": "cicero",
    "antonii": "antonius", "antonium": "antonius", "antonius'": "antonius",
    "crassi": "crassus", "crassum": "crassus",
    # SG
    "römisch": "rom", "römer": "rom",
    "karthagisch": "karthago", "karthager": "karthago",
    "makedonisch": "makedonien" 
}

PROPERNAME_RULE_PREFIXES = {"caesar", "pompeius", "cicero", "antonius", "crassus"}

def load_spacy_model():
    import spacy
    try:
        return spacy.load("de_core_news_sm", disable=["parser", "ner", "tagger"])
    except OSError:
        print("⚠️ Modell 'de_core_news_sm' nicht gefunden. Bitte installieren:\n  python -m spacy download de_core_news_sm")
        sys.exit(1)

def normalize_propername(token_text_lower, lemma_lower, is_propn):
    if token_text_lower in CUSTOM_MAP:
        return CUSTOM_MAP[token_text_lower]
    if lemma_lower in CUSTOM_MAP:
        return CUSTOM_MAP[lemma_lower]

    t = token_text_lower.replace("æ", "ae").replace("œ", "oe")
    if is_propn:
        for pref in PROPERNAME_RULE_PREFIXES:
            if t.startswith(pref) and t.endswith("s") and len(t) - len(pref) <= 3:
                return pref
    return lemma_lower

def analyze_large_text(file_path, top_n=50, chunk_size=200_000):
    nlp = load_spacy_model()
    stopwords = nlp.Defaults.stop_words

    #SG - definieren zusätzlicher Stopwords
    custom_stopwords = {"anderer", "alt", "art", "ähnlich", "allgemein",
                        "bleiben", "bloß", "bringen", "beginnen", "bestehen", "bilden", "bezeichnen",
                        "ding", "dennoch",
                        "einzeln", "erscheinen", "einzig", "eigentlich",
                        "finden", "fast", "früh", "freilich", "fallen", "fest", "fall", "form", "ferner",
                        "geben", "gewiß", "gehören", "gelten",
                        "halten", "hand", "heißen",
                        "indes",
                        "klein",
                        "lassen", "letzter", "liegen", "leben",
                        "mann",
                        "neu", "namentlich", "nehmen", "name", "nennen",
                        "reich",
                        "stehen", "scheinen", "stellen", "setzen", "selber", "schlagen", "sehen", "seite", "sogar", "spät", "schwer", "stark", "sagen", "sicher",
                        "teils", "treten", "treffen", 
                        "unvollständig", "übrig", "ursprünglich",
                        "verhältnis", "vollständig", "vielmehr",
                        "wesentlich", "weise", "weg", "weder", "ward", "wichtig", "wahrscheinlich", 
                        "ziehen", "zeigen"
                        }
    stopwords = stopwords.union(custom_stopwords)


    text = Path(file_path).read_text(encoding="utf-8")

    lemmas = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        doc = nlp(chunk)
        for token in doc:
            if not token.is_alpha:
                continue
            lemma = normalize_propername(token.text.lower(), token.lemma_.lower(), token.pos_ == "PROPN")
            if lemma not in stopwords and len(lemma) > 2:
                lemmas.append(lemma)

    # Frequenzen
    freq = Counter(lemmas)
    total = sum(freq.values())
    norm_freq = {w: (c / total) * 1000 for w, c in freq.items()}

    # Ausgabe
    print(f"\nTop {top_n} Lemmata für {Path(file_path).name} (normiert pro 1000 Wörter):\n")
    print(f"{'Lemma':20} {'Count':>8} {'pro 1000 Wörtern':>20}")
    print("-" * 50)
    for w, c in freq.most_common(top_n):
        print(f"{w:20} {c:8d} {norm_freq[w]:20.2f}")

    # CSV speichern
    out_csv = Path(file_path).with_suffix(".freq.csv")
    with open(out_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["lemma", "count", "per_1000"])
        for w, c in freq.most_common():
            writer.writerow([w, c, round(norm_freq[w], 3)])

    print(f"\n✅ Ergebnisse gespeichert: {out_csv.resolve()}")

# ======== MAIN ========

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_text_large.py <input.txt> [--top N]")
        sys.exit(1)

    file_path = sys.argv[1]
    top_n = 200
    if "--top" in sys.argv:
        try:
            top_n = int(sys.argv[sys.argv.index("--top") + 1])
        except:
            pass

    analyze_large_text(file_path, top_n)
