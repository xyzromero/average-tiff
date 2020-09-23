# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 12:28:30 2020

@author: David
"""

from osgeo import gdal
import numpy as np

file_path = []
count = 30
while count > 0:
    file_path.append("C:/Users/51922/Desktop/avg/" + str(count) + ".tif")
    count-=1 
  
# We build one large np array of all images (this requires that all data fits in memory)
res = []
for f in file_path:
    ds = gdal.Open(f)
    res.append(ds.GetRasterBand(1).ReadAsArray()) # We assume that all rasters has a single band
stacked = np.dstack(res) # We assume that all rasters have the same dimensions
mean = np.mean(stacked, axis=-1)

# Finally save a new raster with the result. 
# This assumes that all inputs have the same geotransform since we just copy the first
driver = gdal.GetDriverByName('GTiff')
result = driver.CreateCopy('ETmaps_average.tif', gdal.Open(file_path[0]))
result.GetRasterBand(1).WriteArray(mean)
result = None