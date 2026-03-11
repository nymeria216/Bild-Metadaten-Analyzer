import csv
import json


# Exportiert die Metadaten als CSV-Datei
def als_csv_exportieren(metadaten, ausgabe_pfad):

    with open(ausgabe_pfad, "w", newline="", encoding="utf-8-sig") as datei:

        writer = csv.writer(datei, delimiter=";")

        # Tabellenüberschrift
        writer.writerow(["Feld", "Wert"])

        # Allgemeine Bildinformationen
        writer.writerow(["Datei", metadaten["datei"]])
        writer.writerow(["Format", metadaten["format"]])
        writer.writerow(["Bildgröße", metadaten["groesse"]])
        writer.writerow(["EXIF vorhanden", metadaten["has_exif"]])

        # EXIF-Daten
        for schluessel in metadaten["exif"]:
            writer.writerow([schluessel, metadaten["exif"][schluessel]])


# Exportiert die Metadaten als JSON-Datei
def als_json_exportieren(metadaten, ausgabe_pfad):

    with open(ausgabe_pfad, "w", encoding="utf-8") as datei:

        json.dump(
            metadaten,
            datei,
            indent=4,
            ensure_ascii=False
        )