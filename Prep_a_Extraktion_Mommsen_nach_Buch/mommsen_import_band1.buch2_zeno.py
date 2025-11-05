import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin

BASE_URL = "http://www.zeno.org/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Erster+Band/Zweites+Buch.+Von+der+Abschaffung+des+r%C3%B6mischen+K%C3%B6nigtums+bis+zur+Einigung+Italiens"
OUTPUT_DIR = "Mommsen_Quelltext_Zeno_Band1.Buch2"
os.makedirs(OUTPUT_DIR, exist_ok=True)

kapitel_links = [
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Erster+Band/Zweites+Buch.+Von+der+Abschaffung+des+römischen+Königtums+bis+zur+Einigung+Italiens/Erstes+Kapitel.+Änderung+der+Verfassung.+Beschränkung+der+Magistratsgewalt", # 1
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Erster+Band/Zweites+Buch.+Von+der+Abschaffung+des+römischen+Königtums+bis+zur+Einigung+Italiens/Zweites+Kapitel.+Das+Volkstribunat+und+die+Decemvirn", #2
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Erster+Band/Zweites+Buch.+Von+der+Abschaffung+des+römischen+Königtums+bis+zur+Einigung+Italiens/Drittes+Kapitel.+Die+Ausgleichung+der+Stände+und+die+neue+Aristokratie", #3
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Erster+Band/Zweites+Buch.+Von+der+Abschaffung+des+römischen+Königtums+bis+zur+Einigung+Italiens/Viertes+Kapitel.+Sturz+der+etruskischen+Macht.+Die+Kelten", #4
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Erster+Band/Zweites+Buch.+Von+der+Abschaffung+des+römischen+Königtums+bis+zur+Einigung+Italiens/Fünftes+Kapitel.+Die+Unterwerfung+der+Latiner+und+Kampaner+unter+Rom", #5
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Erster+Band/Zweites+Buch.+Von+der+Abschaffung+des+römischen+Königtums+bis+zur+Einigung+Italiens/Sechstes+Kapitel.+Die+Italiker+gegen+Rom", #6
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Erster+Band/Zweites+Buch.+Von+der+Abschaffung+des+römischen+Königtums+bis+zur+Einigung+Italiens/Siebtes+Kapitel.+König+Pyrrhos+gegen+Rom+und+die+Einigung+Italiens", #7
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Erster+Band/Zweites+Buch.+Von+der+Abschaffung+des+römischen+Königtums+bis+zur+Einigung+Italiens/Achtes+Kapitel.+Recht.+Religion.+Kriegswesen.+Volkswirtschaft.+Nationalität", #8
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Erster+Band/Zweites+Buch.+Von+der+Abschaffung+des+römischen+Königtums+bis+zur+Einigung+Italiens/Neuntes+Kapitel.+Kunst+und+Wissenschaft", #9
    "/Geschichte/M/Mommsen,+Theodor/Römische+Geschichte/Erster+Band/Zweites+Buch.+Von+der+Abschaffung+des+römischen+Königtums+bis+zur+Einigung+Italiens/Fußnoten"  # Fussnoten
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
