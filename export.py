import csv
import json

# Importiert die Export-Funktionen in eine CSV-Datei
def export_to_csv(metadata, output_path):
    # Öffnet/ Erstellt eine CSV-Datei zum Schreiben
    # encoding="utf-8-sig" sorgt dafür, dass Umlaute (Ä, Ö) in Excel korrekt angezeigt werden
    with open(output_path, "w", newline="", encoding="utf-8-sig") as file:
        
        # CSV-Writer erstellen, der Daten mit ; trennt
        writer = csv.writer(file, delimiter=";")

        # Tabellenkopf schreiben
        writer.writerow(["Feld", "Wert"])

        # Allgemeine Bildinformationen in die CSV schreiben
        writer.writerow(["Datei", metadata["datei"]])
        writer.writerow(["Format", metadata["format"]])
        writer.writerow(["Bildgröße", metadata["groesse"]])
        writer.writerow(["EXIF vorhanden", metadata["has_exif"]])

        # Alle vorhandenen EXIF-Daten durchlaufen
        # Jeder EXIF-Eintrag wird als neue Zeile gespeichert
        for key in metadata["exif"]:
            writer.writerow([key, metadata["exif"][key]])

# Importiert die Export-Funktionen in eine JSON-Datei
def export_to_json(metadata, output_path):
    # Öffnet/ Erstellt eine JSON-Datei zum Schreiben
    with open(output_path, "w", encoding="utf-8-sig") as file:
        
        # json.dump schreibt das gesamte Dictionary in die Datei
        # indent=4 ist für eine übersichtliche Formatierung
        # ensure_ascii=False erlaubt die Verwendung von Umlauten
        json.dump(metadata, file, indent=4, ensure_ascii=False)