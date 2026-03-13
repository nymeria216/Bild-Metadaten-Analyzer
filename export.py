import csv
import json


def als_csv_exportieren(metadaten, ausgabe_pfad):
    with open(ausgabe_pfad, "w", newline="", encoding="utf-8-sig") as datei:
        writer = csv.writer(datei, delimiter=";")

        writer.writerow(["Feld", "Wert"])
        writer.writerow(["Datei", str(metadaten["datei"])])
        writer.writerow(["Bildgröße", str(metadaten["groesse"])])
        writer.writerow(["EXIF vorhanden", str(metadaten["has_exif"])])

        for schluessel in metadaten["exif"]:
            writer.writerow([str(schluessel), str(metadaten["exif"][schluessel])])


def als_json_exportieren(metadaten, ausgabe_pfad):
    with open(ausgabe_pfad, "w", encoding="utf-8") as datei:
        json.dump(metadaten, datei, indent=4, ensure_ascii=False)