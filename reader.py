from PIL import Image, ExifTags


def convert_to_degrees(value):
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])

    return d + (m / 60.0) + (s / 3600.0)


def get_gps_info(exif):
    lat = None
    lon = None

    try:
        gps_ifd = exif.get_ifd(ExifTags.IFD.GPSInfo)
    except:
        return None, None

    if not gps_ifd:
        return None, None

    gps_data = {}

    for key in gps_ifd:
        name = ExifTags.GPSTAGS.get(key, key)
        gps_data[name] = gps_ifd[key]

    if "GPSLatitude" in gps_data and "GPSLatitudeRef" in gps_data:
        try:
            lat = convert_to_degrees(gps_data["GPSLatitude"])
            if gps_data["GPSLatitudeRef"] != "N":
                lat = -lat
        except:
            lat = None

    if "GPSLongitude" in gps_data and "GPSLongitudeRef" in gps_data:
        try:
            lon = convert_to_degrees(gps_data["GPSLongitude"])
            if gps_data["GPSLongitudeRef"] != "E":
                lon = -lon
        except:
            lon = None

    return lat, lon


def read_image_metadata(file_path):
    metadata = {}
    metadata["datei"] = file_path
    metadata["format"] = "Nicht vorhanden"
    metadata["groesse"] = "Nicht vorhanden"
    metadata["has_exif"] = False
    metadata["exif"] = {}

    metadata["exif"]["Date/Time"] = "Nicht vorhanden"
    metadata["exif"]["Make"] = "Nicht vorhanden"
    metadata["exif"]["Model"] = "Nicht vorhanden"
    metadata["exif"]["Lens Model"] = "Nicht vorhanden"
    metadata["exif"]["Software"] = "Nicht vorhanden"
    metadata["exif"]["Aperture"] = "Nicht vorhanden"
    metadata["exif"]["Shutter Speed"] = "Nicht vorhanden"
    metadata["exif"]["ISO"] = "Nicht vorhanden"
    metadata["exif"]["Focal Length"] = "Nicht vorhanden"
    metadata["exif"]["GPSLatitude"] = "Nicht vorhanden"
    metadata["exif"]["GPSLongitude"] = "Nicht vorhanden"

    image = Image.open(file_path)

    metadata["format"] = str(image.format)
    metadata["groesse"] = str(image.size[0]) + " x " + str(image.size[1])

    exif = image.getexif()

    if exif:
        found_real_exif = False

        # Normale EXIF-Tags
        for tag_id in exif:
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            value = exif.get(tag_id)

            if tag_name == "DateTimeOriginal":
                metadata["exif"]["Date/Time"] = str(value)
                found_real_exif = True

            elif tag_name == "DateTime" and metadata["exif"]["Date/Time"] == "Nicht vorhanden":
                metadata["exif"]["Date/Time"] = str(value)
                found_real_exif = True

            elif tag_name == "Make":
                metadata["exif"]["Make"] = str(value)
                found_real_exif = True

            elif tag_name == "Model":
                metadata["exif"]["Model"] = str(value)
                found_real_exif = True

            elif tag_name == "Software":
                metadata["exif"]["Software"] = str(value)
                found_real_exif = True

        # Exif-Unterstruktur für Kameraeinstellungen
        try:
            exif_ifd = exif.get_ifd(ExifTags.IFD.Exif)
        except:
            exif_ifd = {}

        if exif_ifd:
            for tag_id in exif_ifd:
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                value = exif_ifd[tag_id]

                if tag_name == "LensModel":
                    metadata["exif"]["Lens Model"] = str(value)
                    found_real_exif = True

                elif tag_name == "FNumber":
                    metadata["exif"]["Aperture"] = str(value)
                    found_real_exif = True

                elif tag_name == "ExposureTime":
                    metadata["exif"]["Shutter Speed"] = str(value)
                    found_real_exif = True

                elif tag_name == "ISOSpeedRatings":
                    metadata["exif"]["ISO"] = str(value)
                    found_real_exif = True

                elif tag_name == "PhotographicSensitivity":
                    metadata["exif"]["ISO"] = str(value)
                    found_real_exif = True

                elif tag_name == "FocalLength":
                    metadata["exif"]["Focal Length"] = str(value)
                    found_real_exif = True

        # GPS-Unterstruktur
        lat, lon = get_gps_info(exif)

        if lat is not None:
            metadata["exif"]["GPSLatitude"] = lat

        if lon is not None:
            metadata["exif"]["GPSLongitude"] = lon

        if found_real_exif:
            metadata["has_exif"] = True

    image.close()

    return metadata