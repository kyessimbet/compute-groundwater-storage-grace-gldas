"""
This script synchronizes GLDAS NetCDF files with GRACE reference times, saving filtered datasets that share the same time steps.

Author: Kamilya Yessimbet
"""




import os
import xarray as xr
import numpy as np


def get_all_times_from_folder(folder_path):
    all_times = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.nc'):
            filepath = os.path.join(folder_path, filename)
            ds = xr.open_dataset(filepath)

            times = ds['time'].values
            all_times.append(times)
            ds.close()

    all_times = np.unique(np.concatenate(all_times))
    return all_times


def filter_files_by_time(source_folder, target_folder, output_folder, reference_times):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(target_folder):
        if filename.endswith('.nc'):
            filepath = os.path.join(target_folder, filename)
            ds = xr.open_dataset(filepath)

            intersect_times = np.intersect1d(ds['time'].values, reference_times)

            if intersect_times.size > 0:

                ds_filtered = ds.sel(time=intersect_times)

                output_path = os.path.join(output_folder, filename)
                ds_filtered.to_netcdf(output_path)
                print(f"Saved filtered data for {filename} with {len(intersect_times)} time steps.")

            ds.close()



folder_with_times =  "./grace_data/grace_interpolated"
folder_to_filter = "./gldas/gldas_processed"
output_filtered_folder = "./gldas/gldas_processed_select_time"


reference_times = get_all_times_from_folder(folder_with_times)
print(f"Reference times extracted: {len(reference_times)}")


filter_files_by_time(folder_with_times, folder_to_filter, output_filtered_folder, reference_times)
