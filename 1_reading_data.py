#!/usr/bin/env python
# coding: utf-8

import os
import gc
import sys
import glob
gc.enable()

#TODO: insert logging configuration

import json
import numpy as np
import xarray as xr

sys.path.append("/vsc-hard-mounts/leuven-data/365/vsc36511/WORK_AREA/CODING")
from pylis import readers


# ----------------------------------------------------------------------------
# aux functions

def lonlat2xy(datarray, x_dim, y_dim, lon_centroid, lat_centroid, lon_1d_u, lat_1d_u):
    x_id = datarray[x_dim][np.abs(lon_1d_u-lon_centroid).argmin()].values.squeeze()
    y_id = datarray[y_dim][np.abs(lat_1d_u-lat_centroid).argmin()].values.squeeze()
    return (int(x_id), int(y_id))

# ----------------------------------------------------------------------------

# read configuration file
config = 'config_reading_data.json'
with open(config, 'r') as f:
    config_dict = json.load(f)

# turn keys from json dict into global variables
for key, value in config_dict.items():
    globals()[key] = value

# additional variables' processing
start_year = start_date.split('/')[-1]
end_year = end_date.split('/')[-1]

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# open and read landcovers in aux file
with open('aux.json', 'r') as file:
    aux_dict = json.load(file)
landcover_classes = aux_dict['Vegetation parameters']['New IGBP_MODIS_BU+tundra Landcover Class Legend']

# loop over the regions defined in configuration file
for i, region in enumerate(region_list):

    output_fn = f'{region}_{start_year}_{end_year}_{vars}.nc'

    # open and read lis_input file to get landcover class of centroid
    ds_input = xr.open_dataset(lis_input_file)
    lon_1d_u = ds_input.lon[0,:].values
    lat_1d_u = ds_input.lat[:,0].values
    x_id, y_id = lonlat2xy(ds_input, 'east_west', 'north_south', lon_centroid[i], lat_centroid[i], lon_1d_u, lat_1d_u)
    landcover_centroid = ds_input.isel(east_west=x_id, north_south=y_id).LANDCOVER.values
    landcover_centroid_class_id = str(np.where(landcover_centroid==1)[0][0]+1) # +1 since python starts with 0 and classes with 1
    landcover_centroid_class = landcover_classes[landcover_centroid_class_id]
    
    if vars == 'all':
        # find and open example output
        lis_dir_file_example = glob.glob(os.path.join(lis_dir, lis_output_pattern))[0]
        ds_example = xr.open_dataset(lis_dir_file_example)
        # extract names of all variables
        var_list = [x for x in ds_example.data_vars if 'tavg' in x or 'inst' in x]
    else:
        var_list = vars
    
    # loop over all variables and append to a list of datasets
    dc_list = []
    dc = None
    for var in var_list:
        # read in soil moisture data cube
        dc = readers.lis_cube(
            lis_dir = lis_dir,
            lis_input_file = lis_input_file,
            var = var,
            start = start_date,
            end = end_date,
            freq = freq,
            date_shift = True
        )
        # datetime   = dc.time.values
        lon_1d_u = dc.lon[0,:].values
        lat_1d_u = dc.lat[:,0].values
        x_id, y_id = lonlat2xy(dc, 'x', 'y', lon_centroid[i], lat_centroid[i], lon_1d_u, lat_1d_u)
        data = dc.isel(x=x_id, y=y_id)
        data.name = var
        dc_list.append(data)
        del dc
    
    dc_tot = xr.merge(dc_list)
    dc_tot.attrs['LANDCOVER'] = landcover_centroid_class
    dc_tot_fn = os.path.join(output_dir, output_fn)
    if os.path.exists(dc_tot_fn):
        os.remove(dc_tot_fn)
    dc_tot.to_netcdf(dc_tot_fn)