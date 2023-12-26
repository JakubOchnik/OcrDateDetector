from easyocr import Reader
from datetime import datetime
import os
from PIL import Image
import cv2
import re

class Picture:
    def __init__(self):
        self.file_name = None
        self.date_taken = None

month_map = {
    "sty": "Jan",
    "lut": "Feb",
    "mar": "Mar",
    "kwi": "Apr",
    "maj": "May",
    "cze": "Jun",
    "lip": "Jul",
    "sie": "Aug",
    "wrz": "Sep",
    "paź": "Oct",
    "lis": "Nov",
    "gru": "Dec"
}

def get_date_from_exif(img_path):
    exif = Image.open(img_path)._getexif()
    if not exif:
        return None
    tags = [36867,  # DateTimeOriginal
            36868,  # DateTimeDigitized
            306]    # DateTime
    for tag in tags:
        date = exif[tag] if tag in exif else None
        if date:
            break

    if date == None: 
        return None
 
    return datetime.strptime('{}'.format(date), '%Y:%m:%d %H:%M:%S')

def get_date_from_image(img_path):
    image = cv2.imread(img_path)
    if image is None:
        return None
    reader = Reader(['pl'], gpu=True)
    results = reader.readtext(image)
    final_date = None
    for (_, text, prob) in results:
        print("Detected: {} prob: {}".format(text, prob))
        res = re.search("[0-9]+/[0-9]+/[0-9]+", text)
        if res:
            final_date = datetime.strptime(res.group(0), '%d/%m/%Y')
            return final_date

        res = re.search("[0-9]+-[a-zA-Z]{3}-[0-9]+", text)
        if res:
            res_str = res.group(0)
            month = re.search("[a-zA-Z]{3}", res_str)
            if month and month.group(0).lower() in month_map:
                re.sub("[a-zA-Z]{3}", month_map[month], res_str)
                final_date = datetime.strptime(res_str, '%d-%b-%Y')
                return final_date
        
        res = re.search("[0-9]+\.[0-9]+\.[0-9]+", text)
        if res:
            return datetime.strptime(res.group(0), '%d.%m.%Y')

def establish_date(image):
    print("Processing {}".format(image))
    date = get_date_from_exif(image)
    if date:
       return date
    return get_date_from_image(image)

if __name__ == "__main__":
    output = []
    for file in os.listdir("."):
        file = file.lower()
        if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
            date = establish_date(file)
            if date:
                pic = Picture()
                pic.date_taken = date
                pic.file_name = file
                output.append(pic)
        else:
            print("Unknown file: %s" % (file))

    for pic in output:
        print("Image: %s Date: %s" % (pic.file_name, pic.date_taken))
