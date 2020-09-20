# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 17:09:32 2020

@author: David
"""

from netCDF4 import Dataset
import rasterio
from rasterio.transform import from_origin
import numpy as np
import glob 

def find_nearest_x(longitude, point_x):
    longitude = np.asarray(longitude)
    idx = (np.abs(longitude - point_x)).argmin()
    return idx
def find_nearest_y(latitude, point_y):
    latitude = np.asarray(latitude)
    dist = (np.abs(latitude - point_y))
    idy = np.where(dist ==dist.min())[0]
    return int(idy)
dir_path = 'C:/Users/51922/Desktop/tiff average/'
output = dir_path + 'output/'
files = sorted(glob.glob(dir_path+'*.nc'))
transform = from_origin(-90, 0, 0.0416, 0.0416)
# Open netCDF-4 file.
j=0
for i in files:
    nc = Dataset(i)
    latitude = nc.variables['lat'][:]
    longitude = nc.variables['lon'][:]
    sst = nc.variables['sea_surface_temperature']
    fillvalue = sst._FillValue
    data = sst[:]
    data = data[0]
    
    posx0 = find_nearest_x(longitude,-90)
    posx1 = find_nearest_x(longitude,-70)
    posy0 = find_nearest_y(latitude,0)
    posy1 = find_nearest_y(latitude,-20)
    y = latitude[posy0:posy1]  # new_x0 = longitude[posx0],new_x1 = longitude[posx1],# new_x1 = longitude[posx1],# new_y1 = latitude[posy1]
    x = longitude[posx0:posx1]
    data_final = data[posy0:posy1,posx0:posx1]
    print(data_final.shape) 
    j=j+1
    
    profile = {'driver': 'GTiff', 'count': 1, 'height': data_final.shape[0], 'width': data_final.shape[1], 'dtype': str(data_final.dtype), 'transform': transform} 
    with rasterio.open(output+str(j)+'.tif', 'w', crs='EPSG:4326', **profile) as dst: 
          dst.write(data_final, indexes=1) 
    
ds = rasterio.open(output+ str(j)+'.tif')     
data = ds.read() 
data[data == fillvalue] = 0
     
