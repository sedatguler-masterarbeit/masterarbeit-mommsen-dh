import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin

BASE_URL = "http://www.zeno.org/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Dritter+Band/F%C3%BCnftes+Buch.+Die+Begr%C3%BCndung+der+Milit%C3%A4rmonarchie"
OUTPUT_DIR = "Mommsen_Quelltext_Zeno_Band3"
os.makedirs(OUTPUT_DIR, exist_ok=True)

kapitel_links = [
    "/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Dritter+Band/F%C3%BCnftes+Buch.+Die+Begr%C3%BCndung+der+Milit%C3%A4rmonarchie/Erstes+Kapitel.+Marcus+Lepidus+und+Quintus+Sertorius", # 1
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Dritter+Band/Fünftes+Buch.+Die+Begründung+der+Militärmonarchie/Zweites+Kapitel.+Die+sullanische+Restaurationsherrschaft", #2
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Dritter+Band/Fünftes+Buch.+Die+Begründung+der+Militärmonarchie/Drittes+Kapitel.+Der+Sturz+der+Oligarchie+und+die+Herrschaft+des+Pompeius", #3
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Dritter+Band/Fünftes+Buch.+Die+Begründung+der+Militärmonarchie/Viertes+Kapitel.+Pompeius+und+der+Osten", #4
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Dritter+Band/Fünftes+Buch.+Die+Begründung+der+Militärmonarchie/Fünftes+Kapitel.+Der+Parteienkampf+während+Pompeius%27+Abwesenheit", #5
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Dritter+Band/Fünftes+Buch.+Die+Begründung+der+Militärmonarchie/Sechstes+Kapitel.+Pompeius%27+Rücktritt+und+die+Koalition+der+Prätendenten", #6
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Dritter+Band/Fünftes+Buch.+Die+Begründung+der+Militärmonarchie/Siebtes+Kapitel.+Die+Unterwerfung+des+Westens", #7
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Dritter+Band/Fünftes+Buch.+Die+Begründung+der+Militärmonarchie/Achtes+Kapitel.+Pompeius%27+und+Caesars+Gesamtherrschaft", #8
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Dritter+Band/Fünftes+Buch.+Die+Begründung+der+Militärmonarchie/Neuntes+Kapitel.+Crassus%27+Tod.+Der+Bruch+der+Gesamtherrscher", #9
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Dritter+Band/Fünftes+Buch.+Die+Begründung+der+Militärmonarchie/Zehntes+Kapitel.+Brundisium,+Ilerda,+Pharsalos+und+Thapsus#google_vignette", #10
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Dritter+Band/Fünftes+Buch.+Die+Begründung+der+Militärmonarchie/Elftes+Kapitel.+Die+alte+Republik+und+die+neue+Monarchie", #11
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Dritter+Band/Fünftes+Buch.+Die+Begründung+der+Militärmonarchie/Zwölftes+Kapitel.+Religion,+Bildung,+Literatur+und+Kunst",  #12
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Dritter+Band/Fünftes+Buch.+Die+Begründung+der+Militärmonarchie/Fußnoten" #13 Fussnoten
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
