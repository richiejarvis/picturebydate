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

def get_exif(image_file_path):
    exif_table = {}
    try:
        image = Image.open(image_file_path)
        info = image.getexif()
        for tag, value in info.items():
            if tag == 36867:
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
            if exif_date_created != None:
                print(str(realEntry) + ": " + str(exif_date_created))
                # Time to get the year/month so we can use those in the new path
                exif_string = str(exif_date_created) 
                newFile = target_dir + "/" + exif_string[22:26] + "/" + exif_string[27:29] + "/" + str(os.path.basename(realEntry))
                print("New location: " + newFile)





if __name__ == "__main__":
    main(sys.argv[1:])



