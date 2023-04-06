# Downloads imagery online and saves locally.

import os
import logging
import sys
from os import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = BASE_DIR + "/"
os.chdir(PROJECT_ROOT)
print(PROJECT_ROOT)
from fpackage.download_data import create_directories, split, download_satellite_image

data_dir = ""


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Prevent logging from propagating to the root logger
        logger.propagate = 0
        console = logging.StreamHandler()
        logger.addHandler(console)
        formatter = logging.Formatter(
            "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        )
        console.setFormatter(formatter)
    return logger


def get_maps_image(filename):
    try:
        GOOGLE_MAPS_API_KEY = environ["GOOGLE_MAPS_API_KEY"]  # set to 'your_API_key'
    except KeyError as e:
        logger.error("Please set your GOOGLE_MAPS_API_KEY environment variable")
        """
        # Hint: 
        Linux
            export GOOGLE_MAPS_API_KEY=AIzaS...........
        Windows
            set GOOGLE_MAPS_API_KEY=AIzaS..............

        """
        sys.exit(1)

    # create the needed directories
    create_directories(data_dir)

    # api key at some point
    api_key = GOOGLE_MAPS_API_KEY  # "AIzaS.........."  # You will need to get your own Google Maps Static Images
    grid_path = PROJECT_ROOT + "Data/grids/"
    image_path = PROJECT_ROOT + "Data/images/"
    split(filename, grid_path)
    download_satellite_image(image_path, grid_path, api_key, filename)


# Path to the GeoJson Feature Extent file of your Region of Interest (ROI)
filename = PROJECT_ROOT + "Input/aoi.geojson"


# Configure logging
logger = get_logger(__name__)
logger.setLevel(logging.INFO)
logger.debug("Errors: {}".format(logging.INFO))

# Function Call
get_maps_image(filename)
