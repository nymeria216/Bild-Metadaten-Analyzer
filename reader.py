from PIL import Image
from PIL.ExifTags import TAGS

IMPORTANT_TAGS = [
    "DateTimeOriginal",
    "Make",
    "Model",
    "LensModel",
    "Software",
    "ExposureTime",
    "FNumber",
    "ISOSpeedRatings",
    "FocalLength",
    "GPSInfo"
]


def read_image_metadata(file_path):

    metadata = {}
    metadata["datei"] = file_path
    metadata["has_exif"] = False
    metadata["exif"] = {}

    image = Image.open(file_path)

    metadata["format"] = image.format
    metadata["groesse"] = str(image.size[0]) + " x " + str(image.size[1])

    exif_data = image.getexif()

    if exif_data:

        for tag_id in exif_data:

            tag_name = TAGS.get(tag_id, tag_id)

            if tag_name in IMPORTANT_TAGS:

                value = exif_data.get(tag_id)
                metadata["exif"][str(tag_name)] = str(value)

        if len(metadata["exif"]) > 0:
            metadata["has_exif"] = True

    image.close()

    return metadata