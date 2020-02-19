import os
import sys
import datetime
import argparse
from PIL import Image, ExifTags

# TODO
#   - Unit tests
#   - More error handling: can't create destination directory, file in use? Inspect for others
#   - Actually copy the file. :)
#   - Is the Exif date always in the format we expect?
#   - Should we also look at other Exif fields?

# Reverse lookup so we can use the friendly string name for the Exif tag
TAGS_reverse = dict(((v, k) for k, v in ExifTags.TAGS.items()))

def get_exif_creation_date(path):
    img = Image.open(path)
    img_exif = img.getexif()
    if img_exif is not None:
        date_time_string = img_exif.get(TAGS_reverse['DateTimeOriginal'])
        if date_time_string:
            return datetime.datetime.strptime(date_time_string, "%Y:%m:%d %H:%M:%S")
    return ""

def get_creation_date(path):
    creation_date = get_exif_creation_date(path)
    if not creation_date:
        # Exif data may not exist, so fallback on the OS creation time.
        timestamp = os.path.getctime(path)
        creation_date = datetime.datetime.fromtimestamp(timestamp)
    return creation_date

def generate_filename(path):
    creation_date = get_creation_date(path)
    creation_date_string = creation_date.strftime("%Y-%m-%d_%H_%M_%S")
    file_extension = os.path.splitext(path)[1]
    return f"{creation_date_string}{file_extension}"

def get_new_path(path, destination_directory):
    new_filename = generate_filename(path)
    return os.path.join(destination_directory, new_filename)

def copy_picture(path, destination_directory):
    if os.path.exists(path):
        new_path = get_new_path(path, destination_directory)
        print(f"{new_path}")
    else:
        print(f"ERROR - File not found: {path}")

def copy_pictures_from_path(source_directory, destination_directory):
    file_list = os.listdir(source_directory)
    for filename in file_list:
        path = os.path.join(source_directory, filename)
        if os.path.isfile(path):
            copy_picture(path, destination_directory)

def copy_pictures_from_text_list(text_list, destination_directory):
    with open(text_list) as text_list_file:
        path_list = text_list_file.read().splitlines()
        for path in path_list:
            copy_picture(path, destination_directory)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sourcedir', help='Source directory of images')
    parser.add_argument('--sourcefile', help='Text file containing a list of images. Optional, and takes precedence over sourcedir')
    parser.add_argument('--destinationdir', help='Destination directory for images')
    args = parser.parse_args()

    destination_directory = r"D:\TestFiles\Destination"
    source_directory = r"D:\TestFiles\Source"

    if args.destinationdir:
        destination_directory = args.destinationdir

    os.makedirs(destination_directory, exist_ok=True)

    if args.sourcefile:
        copy_pictures_from_text_list(args.sourcefile, destination_directory)
    else:
        copy_pictures_from_path(source_directory, destination_directory)

