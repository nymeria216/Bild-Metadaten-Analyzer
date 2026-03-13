from PIL import Image, ExifTags


def wert_zu_float(wert):
    try:
        return float(wert)
    except:
        try:
            return float(wert[0]) / float(wert[1])
        except:
            return None


def bruch_als_text(wert):
    try:
        if hasattr(wert, "numerator") and hasattr(wert, "denominator"):
            return str(wert.numerator) + "/" + str(wert.denominator)

        if isinstance(wert, tuple) and len(wert) == 2:
            return str(wert[0]) + "/" + str(wert[1])

        return str(wert)
    except:
        return str(wert)


def grad_umrechnen(wert):
    if len(wert) < 3:
        return None

    grad = wert_zu_float(wert[0])
    minuten = wert_zu_float(wert[1])
    sekunden = wert_zu_float(wert[2])

    if grad is None or minuten is None or sekunden is None:
        return None

    return grad + (minuten / 60.0) + (sekunden / 3600.0)


def gps_daten_auslesen(exif_daten):
    breitengrad = None
    laengengrad = None

    gps_ifd = None

    try:
        gps_ifd = exif_daten.get_ifd(ExifTags.IFD.GPSInfo)
    except:
        gps_ifd = None

    if not gps_ifd:
        for tag_id in exif_daten:
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            if tag_name == "GPSInfo":
                gps_ifd = exif_daten.get(tag_id)
                break

    if not gps_ifd:
        return None, None

    gps_daten = {}

    for schluessel in gps_ifd:
        name = ExifTags.GPSTAGS.get(schluessel, schluessel)
        gps_daten[name] = gps_ifd[schluessel]

    if "GPSLatitude" in gps_daten and "GPSLatitudeRef" in gps_daten:
        try:
            breitengrad = grad_umrechnen(gps_daten["GPSLatitude"])
            referenz = gps_daten["GPSLatitudeRef"]

            if isinstance(referenz, bytes):
                referenz = referenz.decode(errors="ignore")

            if referenz != "N":
                breitengrad = -breitengrad
        except:
            breitengrad = None

    if "GPSLongitude" in gps_daten and "GPSLongitudeRef" in gps_daten:
        try:
            laengengrad = grad_umrechnen(gps_daten["GPSLongitude"])
            referenz = gps_daten["GPSLongitudeRef"]

            if isinstance(referenz, bytes):
                referenz = referenz.decode(errors="ignore")

            if referenz != "E":
                laengengrad = -laengengrad
        except:
            laengengrad = None

    return breitengrad, laengengrad


def bild_metadaten_auslesen(dateipfad):
    metadaten = {}

    metadaten["datei"] = dateipfad
    metadaten["groesse"] = "Nicht vorhanden"
    metadaten["has_exif"] = False
    metadaten["exif"] = {}

    metadaten["exif"]["Aufnahmedatum"] = "Nicht vorhanden"
    metadaten["exif"]["Hersteller"] = "Nicht vorhanden"
    metadaten["exif"]["Modell"] = "Nicht vorhanden"
    metadaten["exif"]["Objektiv"] = "Nicht vorhanden"
    metadaten["exif"]["Software"] = "Nicht vorhanden"
    metadaten["exif"]["Blende"] = "Nicht vorhanden"
    metadaten["exif"]["Belichtungszeit"] = "Nicht vorhanden"
    metadaten["exif"]["ISO"] = "Nicht vorhanden"
    metadaten["exif"]["Brennweite"] = "Nicht vorhanden"
    metadaten["exif"]["GPS Breitengrad"] = "Nicht vorhanden"
    metadaten["exif"]["GPS Längengrad"] = "Nicht vorhanden"

    bild = Image.open(dateipfad)

    metadaten["groesse"] = str(bild.size[0]) + " x " + str(bild.size[1])

    exif_daten = bild.getexif()

    if exif_daten:
        exif_gefunden = False

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
                    blende = wert_zu_float(wert)
                    if blende is not None:
                        metadaten["exif"]["Blende"] = "f/" + str(round(blende, 2))
                    exif_gefunden = True

                elif tag_name == "ExposureTime":
                    belichtungszeit = wert_zu_float(wert)
                    if belichtungszeit is not None:
                        metadaten["exif"]["Belichtungszeit"] = str(round(belichtungszeit, 6)) + " s"
                    else:
                        metadaten["exif"]["Belichtungszeit"] = bruch_als_text(wert) + " s"
                    exif_gefunden = True

                elif tag_name == "ISOSpeedRatings":
                    metadaten["exif"]["ISO"] = str(wert)
                    exif_gefunden = True

                elif tag_name == "PhotographicSensitivity":
                    metadaten["exif"]["ISO"] = str(wert)
                    exif_gefunden = True

                elif tag_name == "FocalLength":
                    brennweite = wert_zu_float(wert)
                    if brennweite is not None:
                        metadaten["exif"]["Brennweite"] = str(round(brennweite, 2)) + " mm"
                    exif_gefunden = True

        breitengrad, laengengrad = gps_daten_auslesen(exif_daten)

        if breitengrad is not None:
            metadaten["exif"]["GPS Breitengrad"] = str(round(breitengrad, 6))

        if laengengrad is not None:
            metadaten["exif"]["GPS Längengrad"] = str(round(laengengrad, 6))

        if exif_gefunden:
            metadaten["has_exif"] = True

    bild.close()

    return metadaten