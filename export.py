import csv
import json


def export_to_csv(metadata, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")

        writer.writerow(["Feld", "Wert"])
        writer.writerow(["Datei", metadata["datei"]])
        writer.writerow(["Format", metadata["format"]])
        writer.writerow(["Bildgröße", metadata["groesse"]])
        writer.writerow(["EXIF vorhanden", metadata["has_exif"]])

        for key in metadata["exif"]:
            writer.writerow([key, metadata["exif"][key]])


def export_to_json(metadata, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4, ensure_ascii=False)