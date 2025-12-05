from PIL import Image
from PIL.ExifTags import TAGS

image_path = '/Volumes/HSMW_MacOS/Programmierung/3._Semester/Programmierung_II/Bild-Metadaten-Analyzer/img/_DSC7819.jpg'
image = Image.open(image_path)

# EXIF laden
exifdata = image.getexif()

# Liste der gewünschten EXIF-Tags
desired_tags = [
    "Make",
    "Model",
    "DateTime",
    "ExposureTime",
    "FNumber",
    "ISOSpeedRatings",
    "FocalLength"
]

filtered_exif = {}

for tag_id in exifdata:
    tag = TAGS.get(tag_id, tag_id)
    if tag in desired_tags:
        data = exifdata.get(tag_id)

        # Bytes decodieren
        if isinstance(data, bytes):
            try:
                data = data.decode()
            except:
                data = str(data)

        filtered_exif[tag] = data

print(filtered_exif)
