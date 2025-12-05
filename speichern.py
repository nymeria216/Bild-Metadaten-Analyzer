# speichern.py
import csv
import os

import lesen

def speichere_csv(dateiliste, ausgewaehlt, speicherort):
    with open(speicherort, "w", newline="", encoding="utf-8") as f:
        schreiber = csv.writer(f)

        kopf = ["Datei"]
        kopf.extend(ausgewaehlt)
        schreiber.writerow(kopf)

        for datei in dateiliste:
            exif = lesen.hole_exif(datei)

            zeile = [os.path.basename(datei)]

            for tag in ausgewaehlt:
                zeile.append(exif.get(tag, ""))

            schreiber.writerow(zeile)
