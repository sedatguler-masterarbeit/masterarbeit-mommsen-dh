Wordfrequenzanalyse

analyze_text_large.py
Ein einzelnes Textfile pro Lauf, Stopword-Filter, CSV-Ausgabe + Konsolenausgabe.


Absolute Wortfrequenzen sind nur begrenzt vergleichbar, da die Bücher unterschiedlich lang sind.
Besser: relative Worthäufigkeit 


Die 5 Bücher sind unterschiedlich lang, gibt es eine Möglichkeit, die Ergebnisse zu normieren?
Band 1 (120.000 Wörter) vs Band 5 (200.000 Wörter) 
besser: relative Häufigkeit => Anzahl Vorkommen pro 1000 Wörter
Top 20-Begriffe (willkürliche Zahl)

Konsoleninput
python analyze_text_large.py "C:\Mommsen_DH\1_1_Frequenzanalyse\Text_Band1_Buch1_merged.txt" 
python analyze_text_large.py "C:\Mommsen_DH\1_1_Frequenzanalyse\Text_Band1_Buch2_merged.txt"
python analyze_text_large.py "C:\Mommsen_DH\1_1_Frequenzanalyse\Text_Band1_Buch3_merged.txt"
python analyze_text_large.py "C:\Mommsen_DH\1_1_Frequenzanalyse\Text_Band2_Buch4_merged.txt"
python analyze_text_large.py "C:\Mommsen_DH\1_1_Frequenzanalyse\Text_Band3_Buch5_merged.txt" 20

python analyze_text_large.py "C:\Mommsen_DH\1_1_Frequenzanalyse\Text_Band3_Buch5_merged.txt" 20


* Lemmatisierung: „Volk“, „Volkes“, „Volke“, „Völker“, „Völkern“ -> Volk
* Tokenisierung. Originaltext: "Caesar überquerte den Rubikon und begann den Bürgerkrieg."
Tokenisierung: ["Caesar", "überquerte", "den", "Rubikon", "und", "begann", "den", "Bürgerkrieg"]
* Stop Words (= Füllwörter): "und", "der", "die", "das" .. 


Output: 
Text_Band1_Buch1_merged.frq.csv

Lemma                   Count     pro 1000 Wörtern
--------------------------------------------------
rom                       755                22.58
gemeinde                  228                 6.82
griechisch                209                 6.25
latinisch                 174                 5.20
italisch                  168                 5.03
latium                    142                 4.25
italien                   137                 4.10
stadt                     133                 3.98
grieche                   118                 3.53
könig                     115                 3.44
stamm                     113                 3.38
etruskisch                 96                 2.87
bürger                     90                 2.69
haus                       89                 2.66
staat                      88                 2.63
italiker                   87                 2.60
volk                       86                 2.57
etrusker                   82                 2.45
sprache                    73                 2.18
nation                     69                 2.06
entwickelung               67                 2.00
alphabet                   67                 2.00
geschichte                 66                 1.97
latiner                    65                 1.94
gott                       64                 1.91
hellenisch                 63                 1.88
verkehr                    61                 1.82
etrurien                   58                 1.73
geschlecht                 57                 1.71
vater                      56                 1.68
landschaft                 55                 1.65
rechtlich                  54                 1.62
gebiet                     52                 1.56
bürgerschaft               52                 1.56
spur                       50                 1.50
kunst                      48                 1.44
meer                       47                 1.41
uralt                      47                 1.41
epoche                     46                 1.38
zweifel                    45                 1.35
zahl                       45                 1.35
führen                     44                 1.32
politisch                  43                 1.29
götter                     43                 1.29
lateinisch                 42                 1.26
frei                       42                 1.26
fremd                      41                 1.23
bedeutung                  40                 1.20
entwickeln                 39                 1.17
mensch                     39                 1.17


-----
Text_Band1_Buch2_merged.txt
Lemma                   Count     pro 1000 Wörtern

rom                      1136                32.38
gemeinde                  247                 7.04
stadt                     184                 5.24
latinisch                 155                 4.42
könig                     128                 3.65
senat                     127                 3.62
politisch                 117                 3.33
krieg                     112                 3.19
italien                   111                 3.16
konsul                    109                 3.11
griechisch                102                 2.91
italisch                   96                 2.74
etruskisch                 88                 2.51
pyrrhos                    86                 2.45
karthago                   85                 2.42
kampf                      82                 2.34
bürger                     80                 2.28
beamter                    79                 2.25
plebejer                   77                 2.19
gebiet                     77                 2.19
latium                     77                 2.19
heer                       76                 2.17
samnit                     73                 2.08
konsuln                    70                 2.00
gesetz                     70                 2.00
etrurien                   69                 1.97
samnitisch                 66                 1.88
jahrhundert                65                 1.85
tarent                     65                 1.85
volk                       64                 1.82
übrig                      63                 1.80
bürgerschaft               59                 1.68
führen                     58                 1.65
staat                      58                 1.65
samnium                    58                 1.65
nation                     55                 1.57
epoche                     53                 1.51
etrusker                   52                 1.48
gesetzlich                 51                 1.45
adel                       51                 1.45
gewalt                     50                 1.43
sieg                       50                 1.43
verhältnis                 49                 1.40
grieche                    48                 1.37
kampanisch                 48                 1.37
feldherr                   47                 1.34
zweifel                    47                 1.34
eidgenossenschaft          47                 1.34
plebejisch                 46                 1.31
herrschaft                 45                 1.28

-----------
Text_Band1_Buch3_merged.txt
Lemma                   Count     pro 1000 Wörtern

rom                      2180                31.67
karthago                  601                 8.73
krieg                     436                 6.33
stadt                     342                 4.97
hannibal                  284                 4.13
heer                      252                 3.66
makedonien                249                 3.62
griechisch                244                 3.54
italien                   231                 3.36
senat                     209                 3.04
könig                     190                 2.76
italisch                  181                 2.63
gemeinde                  171                 2.48
flotte                    171                 2.48
führen                    165                 2.40
philippos                 160                 2.32
feldherr                  147                 2.14
feind                     141                 2.05
gebiet                    135                 1.96
politisch                 135                 1.96
staat                     132                 1.92
cato                      132                 1.92
schlacht                  130                 1.89
spanien                   124                 1.80
griechenland              122                 1.77
land                      121                 1.76
regierung                 117                 1.70
bürgerschaft              115                 1.67
truppe                    111                 1.61
konsul                    111                 1.61
insel                     109                 1.58
scipio                    108                 1.57
phönikisch                102                 1.48
antiochos                  99                 1.44
schiff                     97                 1.41
erfolg                     96                 1.39
armee                      95                 1.38
nation                     94                 1.37
frieden                    93                 1.35
herr                       89                 1.29
bürger                     88                 1.28
sieg                       85                 1.23
afrika                     83                 1.21
grieche                    82                 1.19
bundesgenosse              81                 1.18
besatzung                  80                 1.16
ätoler                     80                 1.16
feindlich                  79                 1.15
lager                      79                 1.15
kampf                      78                 1.13


-----------
Text_Band2_Buch4_merged.txt

rom                      1594                22.48
senat                     332                 4.68
sulla                     322                 4.54
krieg                     256                 3.61
könig                     249                 3.51
stadt                     230                 3.24
italien                   221                 3.12
politisch                 209                 2.95
konsul                    207                 2.92
gaius                     195                 2.75
italisch                  186                 2.62
teils                     185                 2.61
staat                     177                 2.50
gracchus                  175                 2.47
regierung                 173                 2.44
provinz                   172                 2.43
griechisch                170                 2.40
heer                      170                 2.40
marius                    167                 2.36
gemeinde                  152                 2.14
feldherr                  146                 2.06
gebiet                    145                 2.05
lucius                    134                 1.89
führen                    131                 1.85
gesetz                    126                 1.78
landschaft                124                 1.75
scipio                    122                 1.72
mithradat                 122                 1.72
bürgerschaft              120                 1.69
partei                    110                 1.55
feind                     106                 1.50
bürger                    105                 1.48
spät                      105                 1.48
quintus                   103                 1.45
aristokratie              103                 1.45
militärisch               103                 1.45
hauptstadt                101                 1.42
land                       99                 1.40
metellus                   97                 1.37
soldat                     94                 1.33
armee                      94                 1.33
verfassung                 90                 1.27
revolution                 88                 1.24
tod                        87                 1.23
sklave                     85                 1.20
lager                      84                 1.18
marcus                     84                 1.18
offizier                   84                 1.18
volk                       81                 1.14
kampf                      80                 1.13

-----------
Text_Band3_Buch5_merged.txt

rom                      1501                16.21
caesar                   1267                13.68
pompeius                  747                 8.06
senat                     337                 3.64
könig                     320                 3.45
italien                   263                 2.84
politisch                 257                 2.77
krieg                     256                 2.76
stadt                     224                 2.42
soldat                    222                 2.40
feldherr                  215                 2.32
armee                     212                 2.29
heer                      207                 2.23
provinz                   201                 2.17
partei                    192                 2.07
hauptstadt                188                 2.03
feind                     184                 1.99
legione                   182                 1.96
gebiet                    166                 1.79
italisch                  165                 1.78
gallien                   162                 1.75
führen                    158                 1.71
nation                    156                 1.68
staat                     152                 1.64
landschaft                147                 1.59
griechisch                145                 1.57
truppe                    141                 1.52
gesetz                    135                 1.46
marcus                    134                 1.45
cicero                    134                 1.45
lucullus                  130                 1.40
spanien                   127                 1.37
militärisch               125                 1.35
crassus                   125                 1.35
lager                     125                 1.35
regierung                 124                 1.34
kampf                     120                 1.30
gaius                     118                 1.27
gegner                    116                 1.25
gemeinde                  113                 1.22
demokratie                112                 1.21
land                      112                 1.21
cato                      109                 1.18
keltisch                  108                 1.17
offizier                  107                 1.16
sieg                      106                 1.14
statthalter               106                 1.14
osten                     105                 1.13
gewalt                    103                 1.11
herr                      103                 1.11

