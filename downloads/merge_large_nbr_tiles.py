# Fast way to merge 8000 raster?
# Merge very big number of tiles
# This method does not use for loop for performance reason
# Source:
# 1. https://gis.stackexchange.com/questions/166336/fast-way-to-merge-8000-raster
# 2. https://www.youtube.com/watch?v=sBBMKbAj8XE

import os
import glob
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = BASE_DIR + "/"
# Define your output filename here:
output_filename = PROJECT_ROOT + "Data/rois/nigeria.tif"

# Define your input tiles folder here:
input_path = PROJECT_ROOT + "Data/tiles/{}.tif".format("*")

# First Method


def merge_multiple_tiles(output_filename, input_path):
    """
    Merge very big number of tiles: Fast way to merge 8000 raster?
    """
    os.system(
        "gdal_merge.py -o {output} {input_folder}".format(
            output=output_filename, input_folder=input_path
        )
    )


# First Method


def merge_multiple_tiles_with_subprocess(output_filename, input_path):
    """
    Merge very big number of tiles: Fast way to merge 8000 raster?
    """
    # list all files in directory that match pattern
    all_tiles = glob.glob(input_path)
    cmd = "gdal_merge.py -ps 10 -10 -o {output} {input_folder}".format(
        output=output_filename, input_folder=input_path
    )
    subprocess.call(cmd.split() + all_tiles)


# Function Call
merge_multiple_tiles(output_filename, input_path)
