from PIL import Image, ExifTags

def read_exif_data(image_path):
    img = Image.open(image_path)
    img_exif = img.getexif()

    if not img_exif:
        return {}

    exif_data = {}


    for key, val in img_exif.items():
        tag = ExifTags.TAGS.get(key, key)
        exif_data[tag] = val

    return exif_data
