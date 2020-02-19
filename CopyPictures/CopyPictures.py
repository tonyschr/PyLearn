import os
import sys
import datetime
from PIL import Image, ExifTags

# Reverse lookup so we can use the friendly string name for the Exif tag
_TAGS_r = dict(((v, k) for k, v in ExifTags.TAGS.items()))

def get_exif_creation_date(path):
    img = Image.open(path)
    img_exif = img.getexif()
    if img_exif is not None:
        date_time_string = img_exif.get(_TAGS_r['DateTimeOriginal'])
        if date_time_string:
            return datetime.datetime.strptime(date_time_string, "%Y:%m:%d %H:%M:%S")
    return ""

def get_creation_date(path):
    creation_date = get_exif_creation_date(path)
    if not creation_date:
        timestamp = os.path.getctime(path)
        creation_date = datetime.datetime.fromtimestamp(timestamp)
    return creation_date

def generate_filename(path):
    creation_date = get_creation_date(path)
    creation_date_string = creation_date.strftime("%Y-%m-%d_%H_%M_%S")
    file_extension = os.path.splitext(path)[1]
    return f"{creation_date_string}{file_extension}"

def get_new_path(path):
    new_filename = generate_filename(path)
    return os.path.join(os.path.dirname(path), new_filename)

def copy_picture(path, destination_directory):
    new_path = get_new_path(path)
    print(f"{new_path}")

def copy_pictures_from_path(source_directory, destination_directory):
    file_list = os.listdir(source_directory)
    for filename in file_list:
        path = os.path.join(source_directory, filename)
        if os.path.isfile(path):
            copy_picture(path, destination_directory)

def copy_pictures_from_text_list(text_list, destination_directory):
    return

if __name__ == '__main__':   
    copy_pictures_from_path(r"D:\TestFiles\Source", r"D:\TestFiles\Destination")



        # # { ... 42035: 'FUJIFILM', 42036: 'XF23mmF2 R WR', 42037: '75A14188' ... }
        # for key, val in img_exif_dict.items():
        #     if key in ExifTags.TAGS:
        #         print(f"{ExifTags.TAGS[key]}:{repr(val)}")
        #         # ExifVersion:b'0230'
        #         # ...
        #         # FocalLength:(2300, 100)
        #         # ColorSpace:1
        #         # FocalLengthIn35mmFilm:35
        #         # ...
        #         # Model:'X-T2'
        #         # Make:'FUJIFILM'
        #         # ...
        #         # DateTime:'2019:12:01 21:30:07'
        #         # ...
