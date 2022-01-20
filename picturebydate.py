#!/usr/bin/python3
# This is a simple tool to recursively read a directory, gather a list of files, check whether they are pictures and move them to a new location based upon the date taken.
# 2021 - Richie Jarvis - richie@deepsky.org.uk

from pathlib import Path
#from exif import Image
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import shutil
import sys,getopt
import os
from os.path import exists
import re
from datetime import datetime

def get_exif(image_file_path):
    exif_table = {}
    try:
        image = Image.open(image_file_path)
        info = image.getexif()
        # print (info)
        for tag, value in info.items():
            if tag == 306:
                decoded = TAGS.get(tag, tag)
                exif_table[decoded] = value
                return exif_table
    except:
        return None

def main(argv):
    source_dir = ''
    target_dir = ''
    try:
        opts, args = getopt.getopt(argv,"hs:t:",["source=","target="])
    except getopt.GetoptError:
        print ('test.py -s <source_dir> -t <target_dir')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -s <source_dir> -t <target_dir>')
            sys.exit()
        elif opt in ("-s", "--source"):
            source_dir = arg
        elif opt in ("-t", "--target"):
            target_dir = arg.strip()
    print ('source_dir: ' + source_dir)
    print ('target_dir: ' + target_dir)
    result = list(Path(source_dir).rglob("*"))
    for entry in enumerate(result):
        realEntry = entry[1]
        if realEntry.is_dir() == False:
            exif_date_created = get_exif(realEntry)
            # print(str(realEntry) + ": " + str(exif_date_created))
            if exif_date_created != None:
                # print(str(realEntry) + ": " + str(exif_date_created))
                try:
                    # Time to get the year/month so we can use those in the new path
                    exif_string = str(re.search(r'\d{4}:\d{2}:\d{2}',str(exif_date_created))[0])
                except:
                    exif_string = "0000:00"
                if exif_string != None:
                    year = exif_string[0:4]
                    month = exif_string[5:7]
                    # print(year + "/" + month)
                    target_directory = target_dir + "/" + year + "/" + month + "/" 
                    # target_directory = target_dir + "/" + exif_string[22:26] + "/" + exif_string[27:29] + "/" + str(os.path.basename(realEntry))
                    #print(str(target_directory))
                    target_filename = str(os.path.basename(realEntry))
                    try:
                        os.makedirs(target_directory) # create destination directory, if needed (similar to mkdir -p)
                    except OSError:
                        # The directory already existed, nothing to do
                        pass
                    # Check if the file exists, and suffix with "dup" if a duplicate
                    if exists(target_directory + target_filename):
                        target_filename = target_filename.split(".")
                   #         print(target_filename)
                        target_filename = target_filename[0] + "dup." + target_filename[1]
                    try:
                        # Do the actual move of the file and remove the original
                        shutil.move(str(realEntry),target_directory + target_filename)
                        print("Src: " + str(realEntry) + " Target: " + target_directory + target_filename)
                    except OSError:
                        print("File move failed!!!")
                        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])



