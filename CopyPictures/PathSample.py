import os
import sys
import datetime
import argparse
import shutil
from PIL import Image, ExifTags

# Absolute path including filename of the picture you want to copy.
picture_to_copy = "D:\\SourcePictures\\4-10-2020\\IMG_XYZ123.JPG"

# Absolute path of the destination to copy to
destination_directory = "D:\\FlashDrive\\Album1"

# os.path.split returns a tuple of the head and tail. The head is indexed by [0]
# and the tail by [1]. This gives us just the filename.
#
# D:\\SourcePictures\\4-10-2020\\IMG_XYZ123.JPG
# ^^^^^^^^^^^^^HEAD^^^^^^^^^^^^  ^^^^^TAIL^^^^^
picture_filename = os.path.split(picture_to_copy)[1]
print(f"Picture filename: {picture_filename}")

# os.path.join is essentially the opposite of split: it combines two path segments.
# Here we use it to append the filename to the destination directory, giving an
# absolute path to the new destination.
new_picture_location = os.path.join(destination_directory, picture_filename)
print(f"New picture location: {new_picture_location}")

# Now we can copy 'picture_to_copy' to 'new_picture_location', and we never changed
# global state.
#
# shutil.copy2(picture_to_copy, new_picture_location)