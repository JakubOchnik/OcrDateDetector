# OcrDateDetector
Do you own a collection of scanned pictures with a date stamp, but you're too lazy to manually order them? If so, the OcrDateDetector is just for you!
OcrDateDetector is a Python script that automatically detects the creation date of pictures and renames them to a specified format.

## Features
- Bulk processing of all images in a directory and automatic renaming
- Date detection using OCR or EXIF metadata (if available, useful for mixed digital and scanned photos) 
- Configurable output file name

## Installation
```
# (Optional) Create and activate a new virtual environment
pip install -r requirements.txt
ocr-date-detector -h # Run the program with selected options
```

## Options and usage
```
Usage: ocr-date-detector [OPTIONS] DIRECTORY

Options:
  --ocr BOOLEAN           Use OCR for detection  [default: False]
  --ocr_optimize BOOLEAN  Perform OCR on the bottom right corner of the image
                          first  [default: True]
  --gpu BOOLEAN           Use GPU for enhanced OCR performance  [default:
                          False]
  --exif BOOLEAN          Try to detect date from EXIF metadata (if available)
                          [default: True]
  --name_pattern TEXT     File name format. Placeholders: {date}, {name}
                          [default: img_{date}]
  --verbose BOOLEAN       Print debug logs  [default: False]
  -h, --help              Show this message and exit.
```
