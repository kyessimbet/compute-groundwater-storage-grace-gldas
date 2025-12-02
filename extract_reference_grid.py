"""
This script extracts latitude and longitude coordinates from a GLDAS NetCDF file,
builds a full spatial grid, flattens it into column format,
and saves the reference grid as a CSV file for interpolation of GRACE data.

Author: Kamilya Yessimbet
"""


import xarray as xr
import numpy as np
import pandas as pd


nc_file = "./gldas_data/GLDAS_NOAH025_M.A202505.021.nc4"


ds = xr.open_dataset(nc_file)


lat_name = None
lon_name = None

for var in ds.variables:
    if 'lat' in var.lower():
        lat_name = var
    if 'lon' in var.lower():
        lon_name = var

if lat_name is None or lon_name is None:
    raise ValueError("Could not find latitude and longitude variables in dataset.")

lat = ds[lat_name].values
lon = ds[lon_name].values


if lat.ndim == 1 and lon.ndim == 1:
    lon_grid, lat_grid = np.meshgrid(lon, lat)
else:

    lat_grid = lat
    lon_grid = lon


lat_flat = lat_grid.flatten()
lon_flat = lon_grid.flatten()


grid_df = pd.DataFrame({'lat': lat_flat, 'lon': lon_flat})
grid_df.to_csv("reference_grid.csv", index=False)

print("Grid saved to reference_grid.csv")
