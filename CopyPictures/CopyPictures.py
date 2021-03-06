import os
import sys
import datetime
import argparse
import shutil
from PIL import Image, ExifTags

# TODO:
#   - Unit and/or functional tests
#   - More error handling probably
#   - Remove default test values
#   - Should we also look for Exif fields other than DateTimeOriginal?
#
# Future Features:
#   - Allow the user to specify a minimum rating when copying
#   - Scope to certain file types to avoid copying RAW files, movies, etc. 
#     Could be an optional command line parameter, with copying only JPG
#     being the default

# Reverse lookup so we can use the friendly string name for the Exif tag
TAGS_reverse = dict(((value, key) for key, value in ExifTags.TAGS.items()))

def get_exif_creation_date(path):
    try:
        img = Image.open(path)
        img_exif = img.getexif()
        if img_exif:
            date_time_string = img_exif.get(TAGS_reverse['DateTimeOriginal'])
            if date_time_string:
                # Right now we always expect this format. Need to understand whether there could
                # be others.
                return datetime.datetime.strptime(date_time_string, "%Y:%m:%d %H:%M:%S")
    except Image.UnidentifiedImageError:
        # It's OK if we can't get Exif information because the file type isn't a supported image.
        # For now we copy anyway.
        pass
    return None

def get_creation_date(path):
    creation_date = get_exif_creation_date(path)
    if not creation_date:
        # Exif data may not exist, so fallback on the OS creation time.
        timestamp = os.path.getmtime(path)
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
        print(f"Copying {path} to {new_path}...")
        shutil.copy2(path, new_path)
    else:
        print(f"ERROR - File not found: {path}")

def copy_pictures_from_path(source_directory, destination_directory, recursive):        
    file_list = os.listdir(source_directory)
    for filename in file_list:
        path = os.path.join(source_directory, filename)
        if os.path.isfile(path):
            copy_picture(path, destination_directory)
        elif os.path.isdir(path) and recursive:
            copy_pictures_from_path(path, destination_directory, recursive)

def copy_pictures_from_text_list(text_list, destination_directory):
    with open(text_list) as text_list_file:
        path_list = text_list_file.read().splitlines()
        for path in path_list:
            copy_picture(path, destination_directory)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Copies a set of pictures from either a folder or as specified in a text file.")
    parser.add_argument('--sourcedir', help='Source directory of images')
    parser.add_argument('--sourcefile', help='Text file containing a list of images. Optional, and takes precedence over sourcedir')
    parser.add_argument('--destinationdir', help='Destination directory for images')
    parser.add_argument('--recursive', action="store_true", help='When used with --sourcedir, recurses into subfolders')
    args = parser.parse_args()

    destination_directory = r"D:\TestFiles\Destination"
    source_directory = r"D:\TestFiles\Source"

    if args.sourcedir:
        source_directory = args.sourcedir
    if args.destinationdir:
        destination_directory = args.destinationdir

    try:
        os.makedirs(destination_directory, exist_ok=True)
    except OSError:
        print(f"ERROR - Unable to create destination directory: {destination_directory}")
        exit()

    if args.sourcefile:
        if os.path.exists(args.sourcefile):
            copy_pictures_from_text_list(args.sourcefile, destination_directory)
        else:
            print(f"ERROR - Source text file does not exist: {args.sourcefile}")
    else:
        if os.path.exists(source_directory):
            copy_pictures_from_path(source_directory, destination_directory, args.recursive)
        else:
            print(f"ERROR - Source directory does not exist: {source_directory}")