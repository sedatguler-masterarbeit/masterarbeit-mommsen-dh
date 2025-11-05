import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin

BASE_URL = "http://www.zeno.org/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Erster+Band/Drittes+Buch.+Von+der+Einigung+Italiens+bis+auf+die+Unterwerfung+Karthagos+und+der+Griechischen+Staaten"
OUTPUT_DIR = "Mommsen_Quelltext_Zeno_Band1.Buch3"
os.makedirs(OUTPUT_DIR, exist_ok=True)

kapitel_links = [
    "/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Erster+Band/Drittes+Buch.+Von+der+Einigung+Italiens+bis+auf+die+Unterwerfung+Karthagos+und+der+Griechischen+Staaten/Erstes+Kapitel.+Karthago", # 1
    "/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Erster+Band/Drittes+Buch.+Von+der+Einigung+Italiens+bis+auf+die+Unterwerfung+Karthagos+und+der+Griechischen+Staaten/Zweites+Kapitel.+Der+Krieg+um+Sizilien+zwischen+Rom+und+Karthago", #2
    "/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Erster+Band/Drittes+Buch.+Von+der+Einigung+Italiens+bis+auf+die+Unterwerfung+Karthagos+und+der+Griechischen+Staaten/Drittes+Kapitel.+Die+Ausdehnung+Italiens+bis+an+seine+natürlichen+Grenzen", #3
    "/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Erster+Band/Drittes+Buch.+Von+der+Einigung+Italiens+bis+auf+die+Unterwerfung+Karthagos+und+der+Griechischen+Staaten/Viertes+Kapitel.+Hamilkar+und+Hannibal", #4
    "/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Erster+Band/Drittes+Buch.+Von+der+Einigung+Italiens+bis+auf+die+Unterwerfung+Karthagos+und+der+Griechischen+Staaten/Fünftes+Kapitel.+Der+hannibalische+Krieg+bis+zur+Schlacht+bei+Cannae", #5
    "/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Erster+Band/Drittes+Buch.+Von+der+Einigung+Italiens+bis+auf+die+Unterwerfung+Karthagos+und+der+Griechischen+Staaten/Sechstes+Kapitel.+Der+hannibalische+Krieg+von+Cannae+bis+Zama", #6
    "/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Erster+Band/Drittes+Buch.+Von+der+Einigung+Italiens+bis+auf+die+Unterwerfung+Karthagos+und+der+Griechischen+Staaten/Siebtes+Kapitel.+Der+Westen+vom+hannibalischen+Frieden+bis+zum+Ende+der+dritten+Periode", #7
    "/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Erster+Band/Drittes+Buch.+Von+der+Einigung+Italiens+bis+auf+die+Unterwerfung+Karthagos+und+der+Griechischen+Staaten/Achtes+Kapitel.+Die+östlichen+Staaten+und+der+zweite+makedonische+Krieg", #8
    "/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Erster+Band/Drittes+Buch.+Von+der+Einigung+Italiens+bis+auf+die+Unterwerfung+Karthagos+und+der+Griechischen+Staaten/Neuntes+Kapitel.+Der+Krieg+gegen+Antiochos+von+Asien", #9
    "/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Erster+Band/Drittes+Buch.+Von+der+Einigung+Italiens+bis+auf+die+Unterwerfung+Karthagos+und+der+Griechischen+Staaten/Zehntes+Kapitel.+Der+dritte+makedonische+Krieg", #10
    "/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Erster+Band/Drittes+Buch.+Von+der+Einigung+Italiens+bis+auf+die+Unterwerfung+Karthagos+und+der+Griechischen+Staaten/Elftes+Kapitel.+Regiment+und+Regierte", #11
    "/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Erster+Band/Drittes+Buch.+Von+der+Einigung+Italiens+bis+auf+die+Unterwerfung+Karthagos+und+der+Griechischen+Staaten/Zwölftes+Kapitel.+Boden-+und+Geldwirtschaft", #12
    "/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Erster+Band/Drittes+Buch.+Von+der+Einigung+Italiens+bis+auf+die+Unterwerfung+Karthagos+und+der+Griechischen+Staaten/Dreizehntes+Kapitel.+Glaube+und+Sitte", #13
    "/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Erster+Band/Drittes+Buch.+Von+der+Einigung+Italiens+bis+auf+die+Unterwerfung+Karthagos+und+der+Griechischen+Staaten/Vierzehntes+Kapitel.+Literatur+und+Kunst", #14
    "/Geschichte/M/Mommsen,+Theodor/R%C3%B6mische+Geschichte/Erster+Band/Drittes+Buch.+Von+der+Einigung+Italiens+bis+auf+die+Unterwerfung+Karthagos+und+der+Griechischen+Staaten/Fußnoten"  # Fussnoten
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
