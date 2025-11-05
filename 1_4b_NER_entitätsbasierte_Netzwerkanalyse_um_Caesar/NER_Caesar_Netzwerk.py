# Mommsen_Buch5_NER_Netzwerk_thinned.py
# Gedünntes Netzwerk: Caesar im Zentrum, lesbar

from pathlib import Path
import spacy
import pandas as pd
import itertools
import networkx as nx
import matplotlib.pyplot as plt

# -----------------------------
# 1. Pfade
# -----------------------------
data_folder = Path("c:/mommsen_dh/1_4b_NER_entitätsbasierte_Netzwerkanalyse_um_Caesar")
input_file = data_folder / "Buch5.txt"
output_edges_file = data_folder / "Mommsen_Buch5_edges_thinned.csv"
output_network_png = data_folder / "Mommsen_Buch5_Netzwerk_thinned.png"

# -----------------------------
# 2. Sprachmodell laden
# -----------------------------
nlp = spacy.load("de_core_news_lg", disable=["parser","tagger"])
if "sentencizer" not in nlp.pipe_names:
    nlp.add_pipe("sentencizer")

# -----------------------------
# 3. Text in Blöcke teilen
# -----------------------------
def split_text(text, max_length=80000):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

text = input_file.read_text(encoding="utf-8")
chunks = split_text(text)

sent_entities = []

for i, chunk in enumerate(chunks):
    doc = nlp(chunk)
    for sent in doc.sents:
        ents = []
        for ent in sent.ents:
            if ent.label_ in ["PER", "LOC", "GPE", "ORG"]:
                ents.append((ent.text.strip(), ent.label_))
        if ents:
            sent_entities.append(ents)
    print(f"Chunk {i+1}/{len(chunks)} verarbeitet")

# -----------------------------
# 4. Co-Occurrence-Kanten
# -----------------------------
edges = []
for ents in sent_entities:
    unique_ents = list({e[0]: e for e in ents}.values())
    for (a, a_type), (b, b_type) in itertools.combinations(unique_ents, 2):
        edges.append((a, b, a_type, b_type))

df_edges = pd.DataFrame(edges, columns=["Source", "Target", "Type_Source", "Type_Target"])
df_edges["Weight"] = 1
edges_grouped = df_edges.groupby(["Source","Target","Type_Source","Type_Target"]).count().reset_index()

# Kanten filtern: nur Gewicht ≥3
edges_filtered = edges_grouped[edges_grouped["Weight"] >= 3]
edges_filtered.to_csv(output_edges_file, index=False, encoding="utf-8")
print(f"Kanten gespeichert: {len(edges_filtered)} → {output_edges_file}")

# -----------------------------
# 5. Netzwerk aufbauen
# -----------------------------
G = nx.from_pandas_edgelist(
    edges_filtered,
    source="Source",
    target="Target",
    edge_attr="Weight",
    create_using=nx.Graph()
)

# Knotentyp hinzufügen
node_types = {}
for _, row in edges_filtered.iterrows():
    node_types[row["Source"]] = row["Type_Source"]
    node_types[row["Target"]] = row["Type_Target"]
nx.set_node_attributes(G, node_types, "Type")

# -----------------------------
# 6. Zentralität
# -----------------------------
centrality = nx.degree_centrality(G)
nx.set_node_attributes(G, centrality, "Centrality")

# -----------------------------
# 7. Subgraph: Caesar + direkt verbundene Knoten
# -----------------------------
main_character = "Caesar"
if main_character in G:
    neighbors = list(G.neighbors(main_character)) + [main_character]
    G_focus = G.subgraph(neighbors).copy()
else:
    G_focus = G.copy()

# -----------------------------
# 8. Visualisierung
# -----------------------------
# Farben
color_map = []
for node in G_focus.nodes():
    t = G_focus.nodes[node].get("Type","")
    if t == "PER":
        color_map.append("tomato")
    elif t in ["LOC","GPE"]:
        color_map.append("skyblue")
    elif t == "ORG":
        color_map.append("lightgray")
    else:
        color_map.append("white")

# Größen
sizes = [3000*centrality.get(n,0.01) for n in G_focus.nodes()]
edges_width = [G_focus[u][v]["Weight"]*0.5 for u,v in G_focus.edges()]

# Layout
pos = nx.kamada_kawai_layout(G_focus)

plt.figure(figsize=(14,10))
nx.draw_networkx_nodes(G_focus,pos,node_color=color_map,node_size=sizes,alpha=0.9)
nx.draw_networkx_edges(G_focus,pos,width=edges_width,alpha=0.5)
nx.draw_networkx_labels(G_focus,pos,font_size=10)

plt.title("Mommsen, Römische Geschichte, Buch 5 – Caesar im Zentrum (gedünntes Netzwerk)")
plt.axis("off")
plt.tight_layout()
plt.savefig(output_network_png,dpi=300)
plt.show()

# -----------------------------
# 9. Top-Knoten
# -----------------------------
print("\nTop 15 zentrale Figuren/Entitäten:")
for n, c in sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"{n:25s}  Centrality={c:.3f}")

