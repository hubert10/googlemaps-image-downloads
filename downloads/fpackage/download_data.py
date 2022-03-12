import geopandas as gpd
from shapely.geometry import Polygon
import requests  # To be added
import os
from os import listdir
from os.path import join
from os.path import isfile
from tkinter import Tcl
import rasterio as rio
from rasterio.merge import merge


def create_directories(data_dir):
    # Folder where data for running the notebook is stored
    DATA_FOLDER = os.path.join(data_dir, "Data")
    subfolder_names = ["grids", "images", "tiles", "rois"]
    for subfolder_name in subfolder_names:
        os.makedirs(os.path.join(DATA_FOLDER, subfolder_name), exist_ok=True)

    print("All needed directories successfully created for this workflow")


def split(filename, save_path):
    points = gpd.read_file(filename)
    xmin, ymin, xmax, ymax = points.total_bounds
    c = 0.000125
    c = (points["geometry"].centroid.y)[0]
    k = int(c - 9)
    v = 0.0001
    if k > 1:
        r = 0.0032587421369822628 - (v * ((c - 9) / 10))
    if k == 0:
        r = 0.0032587421369822628
    if k < 1:
        r = 0.0032587421369822628 + (v * ((c - 9) / 10))
    # r=0.002879535403237635
    p = 0.0034332275390625
    # r=0.0034332275390625
    # p=0.003274992640974972
    c = 0.000125
    radu = (ymax - ymin) / r
    radui = (xmax - xmin) / p
    polygon = []
    x = int(radu) + 1
    y = int(radui) + 1
    for i in range(x):  # for y in radu=
        for j in range(y):  # for x in radui=
            polygon.append(
                Polygon(
                    [
                        (xmin + (j * p), ymin + (i * r) - c),
                        (xmin + (j * p), ymin + ((i + 1) * r)),
                        (xmin + ((j + 1) * p), ymin + ((i + 1) * r)),
                        (xmin + ((j + 1) * p), ymin + (i * r) - c),
                    ]
                )
            )

    grid = gpd.GeoDataFrame({"geometry": polygon})
    grid.crs = points.crs
    grid.to_file(save_path + "{}.shp".format(filename.split("/")[-1].split(".")[0]))


# Downloading the grid images
def download_satellite_image(out_path, save_path, api_key, filename):
    """
    Downloads images from Google Maps Static API
    Link: https://developers.google.com/maps/documentation/maps-static/overview 
    """
    db = gpd.read_file(
        save_path + "{}.shp".format(filename.split("/")[-1].split(".")[0])
    )
    print(db.crs)
    db["x"] = db["geometry"].centroid.x
    db["y"] = db["geometry"].centroid.y
    X = db["x"]
    Y = db["y"]
    for i in range(len(db["x"])):
        base_url = "http://maps.googleapis.com/maps/api/staticmap?v=3.44&key={}&center={},{}&scale=2&format=jpg&zoom=18&size=1024x1024&sensor=false&maptype=satellite"
        url = base_url.format(api_key, Y[i], X[i])
        img = open(out_path + "image_{}.jpg".format(int(i)), "wb")
        print("You still have {} images to process".format(len(db["x"]) - i))
        img.write(requests.get(url).content)
        img.close()


def merge_google(path, path_out):
    """"
    Merge Multiple tiles with maximum number of of 1024 or 4096
    after updating ulimit -n (Limited number of files to upload on in Linux)
    
    """
    nlyTIFF = [
        os.path.join(path, f)
        for f in listdir(path)
        if isfile(join(path, f)) and f.endswith(".tif")
    ]
    nlyTIFF = Tcl().call("lsort", "-dict", nlyTIFF)
    # List for the source files
    src_files_to_mosaic = []
    # Iterate over raster files and add them to source -list in 'read mode'
    for fp in nlyTIFF:
        src = rio.open(fp)
        src_files_to_mosaic.append(src)
    mosaic, out_trans = merge(src_files_to_mosaic)
    # Copy the metadata
    out_meta = src.meta.copy()
    # Update the metadata
    out_meta.update(
        {
            "driver": "GTiff",
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": out_trans,
        }
    )
    with rio.open(path_out, "w", **out_meta) as dest:
        dest.write(mosaic)
