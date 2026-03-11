from PIL import Image, ExifTags


# wandelt GPS-Koordinaten von Grad/Minuten/Sekunden in Dezimalgrad um.
def grad_umrechnen(wert):
    grad = float(wert[0])
    minuten = float(wert[1])
    sekunden = float(wert[2])

    return grad + (minuten / 60.0) + (sekunden / 3600.0)


# liest die GPS-Daten aus den EXIF-Daten aus
def gps_daten_auslesen(exif_daten):

    breitengrad = None
    laengengrad = None

    try:
        gps_ifd = exif_daten.get_ifd(ExifTags.IFD.GPSInfo)
    except:
        return None, None

    if not gps_ifd:
        return None, None

    gps_daten = {}

    # GPS-Tags in verständliche Namen umwandeln
    for schluessel in gps_ifd:
        name = ExifTags.GPSTAGS.get(schluessel, schluessel)
        gps_daten[name] = gps_ifd[schluessel]

    # Breitengrad berechnen
    if "GPSLatitude" in gps_daten and "GPSLatitudeRef" in gps_daten:
        try:
            breitengrad = grad_umrechnen(gps_daten["GPSLatitude"])

            if gps_daten["GPSLatitudeRef"] != "N":
                breitengrad = -breitengrad
        except:
            breitengrad = None

    # Längengrad berechnen
    if "GPSLongitude" in gps_daten and "GPSLongitudeRef" in gps_daten:
        try:
            laengengrad = grad_umrechnen(gps_daten["GPSLongitude"])

            if gps_daten["GPSLongitudeRef"] != "E":
                laengengrad = -laengengrad
        except:
            laengengrad = None

    return breitengrad, laengengrad


# Hauptfunktion zum Auslesen der Bild-Metadaten
def bild_metadaten_auslesen(dateipfad):

    metadaten = {}

    # Allgemeine Bildinformationen
    metadaten["datei"] = dateipfad
    metadaten["format"] = "Nicht vorhanden"
    metadaten["groesse"] = "Nicht vorhanden"
    metadaten["has_exif"] = False
    metadaten["exif"] = {}

    # Standardwerte setzen
    metadaten["exif"]["Aufnahmedatum"] = "Nicht vorhanden"
    metadaten["exif"]["Hersteller"] = "Nicht vorhanden"
    metadaten["exif"]["Modell"] = "Nicht vorhanden"
    metadaten["exif"]["Objektiv"] = "Nicht vorhanden"
    metadaten["exif"]["Software"] = "Nicht vorhanden"
    metadaten["exif"]["Blende"] = "Nicht vorhanden"
    metadaten["exif"]["Belichtungszeit"] = "Nicht vorhanden"
    metadaten["exif"]["ISO"] = "Nicht vorhanden"
    metadaten["exif"]["Brennweite"] = "Nicht vorhanden"
    metadaten["exif"]["GPSLatitude"] = "Nicht vorhanden"
    metadaten["exif"]["GPSLongitude"] = "Nicht vorhanden"

    bild = Image.open(dateipfad)

    # Bildformat und Größe bestimmen
    metadaten["format"] = str(bild.format)
    metadaten["groesse"] = str(bild.size[0]) + " x " + str(bild.size[1])

    exif_daten = bild.getexif()

    if exif_daten:
        exif_gefunden = False

        # Normale EXIF-Daten durchsuchen
        for tag_id in exif_daten:
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            wert = exif_daten.get(tag_id)

            if tag_name == "DateTimeOriginal":
                metadaten["exif"]["Aufnahmedatum"] = str(wert)
                exif_gefunden = True

            elif tag_name == "DateTime" and metadaten["exif"]["Aufnahmedatum"] == "Nicht vorhanden":
                metadaten["exif"]["Aufnahmedatum"] = str(wert)
                exif_gefunden = True

            elif tag_name == "Make":
                metadaten["exif"]["Hersteller"] = str(wert)
                exif_gefunden = True

            elif tag_name == "Model":
                metadaten["exif"]["Modell"] = str(wert)
                exif_gefunden = True

            elif tag_name == "Software":
                metadaten["exif"]["Software"] = str(wert)
                exif_gefunden = True

        # Erweiterte Kameraeinstellungen auslesen
        try:
            exif_ifd = exif_daten.get_ifd(ExifTags.IFD.Exif)
        except:
            exif_ifd = {}

        if exif_ifd:
            for tag_id in exif_ifd:
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                wert = exif_ifd[tag_id]

                if tag_name == "LensModel":
                    metadaten["exif"]["Objektiv"] = str(wert)
                    exif_gefunden = True

                elif tag_name == "FNumber":
                    metadaten["exif"]["Blende"] = str(wert)
                    exif_gefunden = True

                elif tag_name == "ExposureTime":
                    metadaten["exif"]["Belichtungszeit"] = str(wert)
                    exif_gefunden = True

                elif tag_name == "ISOSpeedRatings":
                    metadaten["exif"]["ISO"] = str(wert)
                    exif_gefunden = True

                elif tag_name == "PhotographicSensitivity":
                    metadaten["exif"]["ISO"] = str(wert)
                    exif_gefunden = True

                elif tag_name == "FocalLength":
                    metadaten["exif"]["Brennweite"] = str(wert)
                    exif_gefunden = True

        # GPS-Daten auslesen
        breitengrad, laengengrad = gps_daten_auslesen(exif_daten)

        if breitengrad is not None:
            metadaten["exif"]["GPSLatitude"] = breitengrad

        if laengengrad is not None:
            metadaten["exif"]["GPSLongitude"] = laengengrad

        if exif_gefunden:
            metadaten["has_exif"] = True

    bild.close()

    return metadaten