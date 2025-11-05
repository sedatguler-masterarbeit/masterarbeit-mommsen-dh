If you try to replicate my runs, you may need to adapt the path names i used on my local machine.
My local folder structure and the sequence i executed the python scripts is as follows:

# extraction of Mommsens text from zeno.org and postprocessing to get rid of umlauts etc.  as result, the Mommsens extracts are available as one file per book and in addition, more fine granular, as one .txt file per chapter
C:\Mommsen_DH\Prep_a_Extraktion_Mommsen_nach_Buch,   files: mommsen_import_band1.buch1_zeno.py to mommsen_import_band3.buch5_zeno.py
C:\Mommsen_DH\Prep_b_Postprocessing_Mommsen_Extrakt, files: merge_texts.py, Postprocessing_entfernen_seitenzahlen_buchbesprechung.py

# corresponds to chapter 5.1 of the thesis: frequency analysis, KWIC, NER
C:\Mommsen_DH\1_1_Frequenzanalyse,                                 file: analyze_text_large.py  

C:\Mommsen_DH\1_2_KWIC_Senat_als_Querschnittsbegriff,              file: KWIC_Senat_alle_5_Bücher.py
C:\Mommsen_DH\1_2a_KWIC_Senat_Analyse,                             file: KWIC_Senat_analyze.py

C:\Mommsen_DH\1_3_KWIC_Helden_und_Antihelden,                      file: KWIC_Helden_Antihelden.py
C:\Mommsen_DH\1_3a_KWIC_Helden_und_Antihelden_Analyse,             file: KWIC_Helden_Antihelden.py

C:\Mommsen_DH\1_4a_NER_prestep_count,                              file: NER_prestep_count.py
C:\Mommsen_DH\1_4b_NER_entitätsbasierte_Netzwerkanalyse_um_Caesar, file: NER_Caesar_Netzwerk_lemmatisierung.py
  
# corresponds to chapter 5.2 of the thesis: sentiment analysis and topic modelleing
C:\Mommsen_DH\2_1_Sentimentanalyse_BERT,                           files: BERT_Sentimentanalyse_Bevölkerung.py,      
                                                                          BERT_Sentimentanalyse_Gesamttonalität.py,
                                                                          BERT_Sentimentanalyse_Helden_Antihelden.py
                                                                          
C:\Mommsen_DH\2_2_Topicmodelling_BERTopic,                         file:  Bertopic.py (version 7)

# corresponds to chapter 5.3 of the thesis: stylometry  
C:\Mommsen_DH\3_1_Stilometrie_Mommsen,                             file: Stilometrie_Mommsen.py
  
