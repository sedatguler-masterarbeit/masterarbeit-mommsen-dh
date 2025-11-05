import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin

BASE_URL = "http://www.zeno.org/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Zweiter+Band/Viertes+Buch.+Die+Revolution"
OUTPUT_DIR = "Mommsen_Quelltext_Zeno_Band2.Buch4"
os.makedirs(OUTPUT_DIR, exist_ok=True)

kapitel_links = [
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Zweiter+Band/Viertes+Buch.+Die+Revolution/Erstes+Kapitel.+Die+untertänigen+Landschaften+bis+zu+der+Gracchenzeit", # 1
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Zweiter+Band/Viertes+Buch.+Die+Revolution/Zweites+Kapitel.+Die+Reformbewegung+und+Tiberius+Gracchus", #2
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Zweiter+Band/Viertes+Buch.+Die+Revolution/Drittes+Kapitel.+Die+Revolution+und+Gaius+Gracchus+", #3
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Zweiter+Band/Viertes+Buch.+Die+Revolution/Viertes+Kapitel.+Die+Restaurationsherrschaft", #4
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Zweiter+Band/Viertes+Buch.+Die+Revolution/Fünftes+Kapitel.+Die+Völker+des+Nordens", #5
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Zweiter+Band/Viertes+Buch.+Die+Revolution/Sechstes+Kapitel.+Revolutionsversuch+des+Marius+und+Reformversuch+des+Drusus", #6
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Zweiter+Band/Viertes+Buch.+Die+Revolution/Siebtes+Kapitel.+Die+Empörung+der+italischen+Untertanen+und+die+sulpicische+Revolution", #7
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Zweiter+Band/Viertes+Buch.+Die+Revolution/Achtes+Kapitel.+Der+Osten+und+König+Mithradates", #8
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Zweiter+Band/Viertes+Buch.+Die+Revolution/Neuntes+Kapitel.+Cinna+und+Sulla", #9
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Zweiter+Band/Viertes+Buch.+Die+Revolution/Zehntes+Kapitel.+Die+sullanische+Verfassung", #10
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Zweiter+Band/Viertes+Buch.+Die+Revolution/Elftes+Kapitel.+Das+Gemeinwesen+und+seine+Ökonomie", #11
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Zweiter+Band/Viertes+Buch.+Die+Revolution/Zwölftes+Kapitel.+Nationalität.+Religion.+Erziehung", #12
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Zweiter+Band/Viertes+Buch.+Die+Revolution/Dreizehntes+Kapitel.+Literatur+und+Kunst", #13
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Zweiter+Band/Viertes+Buch.+Die+Revolution/Fußnoten"  # Fussnoten
]

for i, link in enumerate(kapitel_links, 1):
    url = urljoin(BASE_URL, link)
    r = requests.get(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.content, "lxml", from_encoding="utf-8")
    # Alle <p> und <br> berücksichtigen
    text_blocks = []
    for elem in soup.find_all(['p', 'br']):
        # <br> erzeugt Zeilenumbruch
        if elem.name == 'br':
            text_blocks.append("\n")
        else:
            para = elem.get_text(" ", strip=True)
            if para:
                text_blocks.append(para)

    # Zusammenfügen mit doppeltem Zeilenumbruch
    text = "\n\n".join(text_blocks)
    text = re.sub(r'\n{3,}', '\n\n', text)  # zu viele Zeilenumbrüche reduzieren

    filename = os.path.join(OUTPUT_DIR, f"kapitel_{i:02}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Kapitel {i} gespeichert: {filename}")
