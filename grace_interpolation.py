"""
Script for resampling GRACE NetCDF data onto a reference grid of GLDAS.


Author: Kamilya Yessimbet
"""




import os
import pandas as pd
import xarray as xr
import numpy as np


netcdf_folder = "./data/grace/grace_data"
csv_grid_file = "./data/reference_grid.csv"
output_folder = "./output/grace_interpolated"




os.makedirs(output_folder, exist_ok=True)


df_grid = pd.read_csv(csv_grid_file)


ref_lat = sorted(df_grid['lat'].unique())
ref_lon = sorted(df_grid['lon'].unique())


netcdf_files = sorted([
    os.path.join(netcdf_folder, f)
    for f in os.listdir(netcdf_folder)
    if f.endswith('.nc') or f.endswith('.nc4')
])

print(f"Found {len(netcdf_files)} NetCDF files.")

if not netcdf_files:

    exit(1)

for file_path in netcdf_files:
    filename = os.path.basename(file_path)
    print(f"Processing {filename}...")


    ds = xr.open_dataset(file_path)


    if (ds.lon > 180).any():
        ds['lon'] = xr.where(ds['lon'] > 180, ds['lon'] - 360, ds['lon'])


        sorted_lon_indices = np.argsort(ds['lon'].values)
        ds = ds.sortby('lon')


    ds_resampled = ds.interp(lat=ref_lat, lon=ref_lon, method='linear')


    name, ext = os.path.splitext(filename)
    output_file = os.path.join(output_folder, f"{name}_resampled{ext}")

    ds_resampled.to_netcdf(output_file)

    print(f" Saved resampledfiile to: {output_file}")


