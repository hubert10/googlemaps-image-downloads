# Adds metadata to the corresponding tiles

import os
import gdal
from PIL import Image
import geopandas as gpd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = BASE_DIR + "/"
saved_grid_path = PROJECT_ROOT + "Data/grids/"
saved_tiles_path = PROJECT_ROOT + "Data/images/"
print(BASE_DIR)
filename = PROJECT_ROOT + "Input/nigeria.geojson"
# adding the metadata to the jpg images
p = gpd.read_file(
    saved_grid_path + "{}.shp".format(filename.split("/")[-1].split(".")[0])
)

for i in range(len(p.bounds["minx"])):
    img = os.path.join(saved_tiles_path + f"image_{i}.jpg")
    image = Image.open(img)
    l = image.size
    nx = l[0]
    ny = l[1]
    ds = gdal.Open(img)
    xmin, ymin, xmax, ymax = (
        p.bounds["minx"][i],
        p.bounds["miny"][i],
        p.bounds["maxx"][i],
        p.bounds["maxy"][i],
    )
    xres = (xmax - xmin) / float(nx)
    yres = (ymax - ymin) / float(ny)
    geotransform = (
        xmin,
        xres,
        0,
        ymax,
        0,
        -yres,
    )
    ds.SetGeoTransform(geotransform)
    ds = None
    input_path = PROJECT_ROOT + "Data/images/image_{}.jpg".format(i)
    output_path = PROJECT_ROOT + "Data/tiles/tile_{}.tif".format(i)
    os.system(
        "gdal_translate -of Gtiff -a_srs EPSG:4326 {cd} {v}".format(
            cd=input_path, v=output_path
        )
    )
