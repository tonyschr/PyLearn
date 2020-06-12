
import os
import sys
import datetime
import argparse
import shutil
from PIL import Image, ExifTags

def copy_unique_file(source_file, destination_dir):
    """Helper function to copy from a local source file to a destination directory"""
    destination_file = os.path.join(destination_dir, source_file)
    print(f"Copyingss {source_file} to {destination_file}")
    print(f'*** destination_file *** {destination_file}')
    save_destination_file = destination_file
    print('&&&& save_destination_file &&& ' , save_destination_file)
    #g_savepicfn = save_destination_file
    # shutil.copy(source_file, destination_dir)
    test_exifread()         

    g_savepicfn = save_destination_file


def test_exifread():
    print("@@@@@ test_exifread @@@@@")


copy_unique_file("a", "b")
# def show_exif_tags(path):
#     img = Image.open(path)
#     img_exif = img.getexif()
#     img_exif_dict = dict(img_exif)

#     # { ... 42035: 'FUJIFILM', 42036: 'XF23mmF2 R WR', 42037: '75A14188' ... }
#     for key, val in img_exif_dict.items():
#         if key in ExifTags.TAGS:
#             print(f"{ExifTags.TAGS[key]}:{repr(val)}")
