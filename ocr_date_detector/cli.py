import os
import click
from ocr_date_detector.exif import get_date_from_exif
from ocr_date_detector.filename_parser import parse_name_string, get_file_name
from ocr_date_detector.ocr_reader import OcrDetector
from pathlib import Path


# Image formats supported by OpenCV
SUPPORTED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".bmp", ".jp2", ".png", ".tiff", ".tif"]

# A list of languages codes (ISO 639) detected during OCR analysis
# Can be modified, e.g. ["de", "fr"]
OCR_LANGUAGES = ["en", "pl"]

# Month mappings. Used for detecting dates in formats such as "10-Jan-2024"
# Can be modified, e.g. ("Jan") or ("sty", "Januar")...
# Only english month names are recognized by default
MONTH_MAPPING_LOCAL = [
    ("Jan", "sty"),
    ("Feb", "lut"),
    ("Mar", "mar"),
    ("Apr", "kwi"),
    ("May", "maj"),
    ("Jun", "cze"),
    ("Jul", "lip"),
    ("Aug", "sie"),
    ("Sep", "wrz"),
    ("Oct", "paź"),
    ("Nov", "lis"),
    ("Dec", "gru"),
]


def determine_date(src_image_path, use_exif, use_ocr, gpu, ocr_optimize, debug):
    image_path = str(src_image_path)
    print("Processing {}".format(image_path))
    if use_exif:
        date = get_date_from_exif(str(image_path), debug)
        if date:
            return date
    if not use_ocr:
        return
    ocr = OcrDetector(OCR_LANGUAGES, MONTH_MAPPING_LOCAL, gpu, ocr_optimize, debug)
    return ocr.get_date_ocr(image_path)


def rename_file(date, file_path, file_extension, name_tokens):
    output_date = date.strftime("%Y-%m-%d")
    file_name = file_path.stem
    base_name = get_file_name(output_date, file_name, name_tokens)
    if not base_name:
        print("ERROR: Failed to parse the name string")
        base_name = "img_{}".format(output_date)
        return None
    base_directory = file_path.parent if file_path.parent is not None else ""
    full_name = (
        "{}{}".format(base_name, file_extension)
        if not base_directory
        else "{}/{}{}".format(base_directory, base_name, file_extension)
    )

    number = None
    while os.path.isfile(full_name):
        if number is None:
            number = 1
        else:
            number += 1
        full_name = "{}_{}{}".format(base_name, number, file_extension)
    os.rename(file_path, full_name)


class Picture:
    def __init__(self, name, date):
        self.file_name = name
        self.date_taken = date


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], show_default=True)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("--ocr", default=False, help="Use OCR for detection")
@click.option(
    "--ocr_optimize",
    default=True,
    help="Perform OCR on the bottom right corner of the image first",
)
@click.option("--gpu", default=False, help="Use GPU for enhanced OCR performance")
@click.option("--exif", default=True, help="Try to detect date from EXIF metadata (if available)")
@click.option("--name_pattern", default="img_{date}", help="File name format. Placeholders: {date}, {name}")
@click.option("--verbose", default=False, help="Print debug logs")
@click.argument("directory")
def main(ocr, ocr_optimize, gpu, exif, name_pattern, verbose, directory):
    name_tokens = parse_name_string(name_pattern)
    if not name_tokens:
        print("ERROR: Failed to parse the name pattern ('{}')".format(name_pattern))
    output = []
    not_detected = []
    for src_file in Path(directory).glob("*"):
        if src_file.is_dir():
            continue
        file_extension = src_file.suffix
        if file_extension.lower() not in SUPPORTED_IMAGE_EXTENSIONS:
            continue
        date = determine_date(src_file, exif, ocr, gpu, ocr_optimize, verbose)
        if date:
            pic = Picture(src_file, date)
            output.append(pic)
            rename_file(date, src_file, file_extension, name_tokens)
        else:
            not_detected.append(src_file)
    print_summary(output, not_detected)


def print_summary(output, not_detected):
    print("Date successfully detected for files:")
    for pic in output:
        print("Image: %s Date: %s" % (pic.file_name, pic.date_taken))

    if not_detected:
        print("Dates could not be detected for files:")
    for pic in not_detected:
        print(pic)


if __name__ == "__main__":
    main()
