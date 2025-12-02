"""
Compute total soil moisture (0–200 cm) from GLDAS NetCDF files.



Author: Kamilya Yessimbet
"""

import os
import xarray as xr

input_folder = r".\gldas\gldas_data"
output_folder =  r".\gldas\gldas_processed"

os.makedirs(output_folder, exist_ok=True)

nc_files = sorted([os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(".nc4")])

ds = xr.open_mfdataset(nc_files, combine='by_coords')

required_vars = [
    'SoilMoi0_10cm_inst',
    'SoilMoi10_40cm_inst',
    'SoilMoi40_100cm_inst',
    'SoilMoi100_200cm_inst'
]
missing_vars = [v for v in required_vars if v not in ds]
if missing_vars:
    raise ValueError(f"Missing required variables in dataset: {missing_vars}")

total_sm = (
    ds['SoilMoi0_10cm_inst'] +
    ds['SoilMoi10_40cm_inst'] +
    ds['SoilMoi40_100cm_inst'] +
    ds['SoilMoi100_200cm_inst']
)

total_sm.name = 'TotalSoilMoisture_0_200cm'
total_sm.attrs['units'] = 'kg m-2'
total_sm.attrs['long_name'] = 'Total Soil Moisture (0–200 cm)'

output_path = os.path.join(output_folder, 'gldas_total_soil_moisture_0_200cm.nc')
total_sm.to_netcdf(output_path)

print(f" TotAl soil moist saved to: {output_path}")

