from PIL import Image
from datetime import datetime
import os

EXIF_DATE_TAG_IDS = [
    36867,  # DateTimeOriginal
    36868,  # DateTimeDigitized
    306,  # DateTime
]

# Image formats with EXIF support
SUPPORTED_EXIF_EXTENSIONS = [".jpg", ".jpeg", ".tif"]


def get_date_from_exif(img_path, debug=False):
    """
    Retrieves a date from the EXIF metadata.

    Args:
        img_path: A path of the input image
        debug: A boolean controlling additional debug logs

    Returns:
        - A datetime object if the date could be established
        - None otherwise
    """

    _, file_extension = os.path.splitext(img_path)
    if file_extension not in SUPPORTED_EXIF_EXTENSIONS:
        if debug:
            print("WARNING: File extension with no EXIF support: {}".format(img_path))
        return None

    exif = Image.open(img_path).getexif()
    if not exif:
        if debug:
            print("WARNING: Failed to retrieve EXIF data: {}".format(img_path))
        return None
    for tag in EXIF_DATE_TAG_IDS:
        date = exif[tag] if tag in exif else None
        if date:
            break

    if date is None:
        if debug:
            print("WARNING: Date unavailable in EXIF data: {}".format(img_path))
        return None

    return datetime.strptime("{}".format(date), "%Y:%m:%d %H:%M:%S")
