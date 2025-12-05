# lesen.py
from PIL import Image, ExifTags

def hole_exif(pfad):
    exif_dict = {}

    try:
        bild = Image.open(pfad)
        exif = bild.getexif()

        for id in exif:
            name = ExifTags.TAGS.get(id, id)
            wert = exif.get(id)

            if isinstance(wert, bytes):
                try:
                    wert = wert.decode("utf-8")
                except:
                    wert = str(wert)

            exif_dict[name] = wert

    except Exception as fehler:
        print("Fehler beim EXIF holen:", fehler)
        exif_dict["ERROR"] = str(fehler)

    return exif_dict
