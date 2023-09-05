import os
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
from colorama import Fore, Back, Style

# auxilary variables
previous = ""
prevent_duplicate_addition = 1
total_files = 0
total_converted = 0
alreadyPXL = 0

# main function

print(Fore.GREEN + "--BULK IMAGE RENAMER--" + Style.RESET_ALL)
print('''the program scans the given folder and rename all of the jpg files
in it to the google's pixel 5 naming convention. the filename is being
based on the date in the metadata of the picture. if it doesn't
exist, the picture will be skipped\n''')
# the folder path
confirm = 'n'
while (confirm != 'y' and confirm != 'Y'):
    print(Fore.GREEN + "paste the folder path which contains images: " + Style.RESET_ALL)
    dir_path = input()
    print(Style.RESET_ALL + "insert 'y' to confirm selected path, anything else to reenter: " + Fore.GREEN, end="")
    confirm = input()
    print()

# get a list of all files and folders inside that folder
try:
    files_list = os.listdir(dir_path)
# raise an IOError if file cannot be found,or the image cannot be opened.
except IOError:
    print()
    print(Fore.RED, Back.WHITE + "#-#-#-#-#-#- folder path was not found -#-#-#-#-#-#" + Style.RESET_ALL)
    print()
    pass
# iterate over the list
for filename in files_list:
    # skips all the folders and files which are not jpg or jpeg
    # counts the total amount of image files
    if filename[0:3] == "PXL":
        alreadyPXL += 1
        continue
    if filename[-3:].lower() == "jpg" or filename[-4:].lower() == "jpeg":
        total_files += 1
        # creates a raw string which is the full folder path and file name
        full_path = dir_path + "\\" + filename
        # Extract the EXIF metadata
        exif_data = Image.open(full_path).getexif()
        # Search for the DateTimeOriginal tag
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "DateTime":
                if value == "":
                    continue
                # Parse the DateTimeOriginal value into a datetime object
                datetime_original = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                # Parse the datetime object into a costume fomat string
                new_name = datetime_original.strftime("PXL_" + "%Y%m%d_%H%M%S")
                # handles cases when several photos were taken on the same second
                if new_name == previous:
                    new_name = (
                            r"{}".format(new_name)
                            + "_"
                            + r"{}".format(prevent_duplicate_addition)
                    )
                    prevent_duplicate_addition += +1
                else:
                    prevent_duplicate_addition = 1
                previous = datetime_original.strftime("PXL_" + "%Y%m%d_%H%M%S")
                # prints the new name and renaming
                print(new_name)
                new_name = dir_path + "\\" + new_name + ".jpg"
                os.rename(full_path, new_name)
                total_converted += 1
    else:
        continue
print()
print(Fore.GREEN + "DONE!" + Style.RESET_ALL)
print(f"{total_converted}{Fore.GREEN} files were converted in total" + Style.RESET_ALL)
print(
    f"{total_files - total_converted}{Fore.GREEN} files were skipped due to lack of necessary metadata" + Style.RESET_ALL)
print(
    f"{alreadyPXL}{Fore.GREEN} files were already with 'PXL' prefix" + Style.RESET_ALL)
print("**created by meister - 29/3/2023**")
print()

# data used tor testing:
# C:\Users\Omer\Desktop\test
# PXL_20220903_123131431
