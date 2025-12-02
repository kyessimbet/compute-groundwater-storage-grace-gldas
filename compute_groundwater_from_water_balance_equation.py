"""
Compute groundwater storage anomalies using the water balance approach.

This script:
- Loads GRACE Total Water Storage (TWS) anomaly data and GLDAS surface storage components:
  * Canopy water (CanopInt_inst)
  * Soil moisture (0–200 cm total)
  * Snow water equivalent (SWE_inst)
- Defines a baseline climatology (2004–2009) and computes monthly anomalies for each GLDAS component.
- Calculates groundwater storage anomaly (GWS) as:
      GWS = GRACE TWS – (Canopy + Soil Moisture + Snow)
  with GLDAS variables converted from kg/m² to meters, then scaled to centimeters.
- Outputs GWS anomaly datasets in NetCDF format with CF-compliant metadata.

Output:
- NetCDF files saved in ./output_groundwater_data/ containing
  'GW_anomaly_cm' (Groundwater Storage Anomaly in cm) for each year.

Author: Kamilya Yessimbet
"""

import xarray as xr
import os
from datetime import datetime, timezone


tws_dir = r".\grace_data\grace_interpolated"
wcan_file = r".\gldas\gldas_processed\gldas_CanopInt_inst.nc"
wsoi_file = r".\gldas\gldas_processed\gldas_total_soil_moisture_0_200cm.nc"
wsno_file = r".\gldas\gldas_processed_select_time\gldas_SWE_inst.nc"
output_dir = r".\output_groundwater_data\baseline_2004-2009_GW_anomalies_based_on_Grace"

os.makedirs(output_dir, exist_ok=True)


wcan = xr.open_dataset(wcan_file)["CanopInt_inst"]
wsoi = xr.open_dataset(wsoi_file)["TotalSoilMoisture_0_200cm"]
wsno = xr.open_dataset(wsno_file)["SWE_inst"]


baseline_start = "2004-01-01"
baseline_end = "2009-12-31"

def compute_monthly_anomaly(data, start, end):
    baseline = data.sel(time=slice(start, end))
    climatology = baseline.groupby("time.month").mean("time")
    return data.groupby("time.month") - climatology


wcan_anom = compute_monthly_anomaly(wcan, baseline_start, baseline_end)
wsoi_anom = compute_monthly_anomaly(wsoi, baseline_start, baseline_end)
wsno_anom = compute_monthly_anomaly(wsno, baseline_start, baseline_end)


tws = xr.open_mfdataset(
    os.path.join(tws_dir, "*.nc"),
    combine="by_coords",
    data_vars="minimal",
    compat="override"
)["lwe_thickness"]


gws_grace = 100 * (
    tws
    - (wcan_anom.sel(time=tws.time) / 1000)
    - (wsoi_anom.sel(time=tws.time) / 1000)
    - (wsno_anom.sel(time=tws.time) / 1000)
)

gws_grace.name = "GW_anomaly_cm"
gws_grace.attrs.update({
    "units": "cm",
    "long_name": "Groundwater Storage Anomaly (GRACE-derived)",
    "standard_name": "groundwater_storage_anomaly",
    "description": (
        "Derived from GRACE Total Water Storage Anomaly (TWS, in meters) minus anomalies of canopy water, "
        "soil moisture (0–200 cm), and snow water equivalent (SWE) from GLDAS (in kg/m²). "
        "GLDAS components are converted to meters (1 kg/m² = 0.001 m), and final result converted to centimeters."
    ),
    "created_on": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
})

# Drop non-dimension coords like 'month'
gws_grace = gws_grace.reset_coords(drop=True)

# Create dataset
ds_out = xr.Dataset({gws_grace.name: gws_grace})
ds_out.attrs.update({
    "title": "GRACE-Derived Groundwater Storage Anomaly",
    "summary": (
        "Monthly groundwater storage anomaly estimated from GRACE TWS minus GLDAS surface storage components "
        "(canopy, soil moisture, snow) over the baseline 2004–2009."
    ),
    "institution": "NASA / User defined",
    "source": ,
    "history": f"Generated on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC",
    "Conventions": "CF-1.7"
})

# Save
output_file = "GW_anomaly_GRACE_baseline_2004-2009.nc"
output_path = os.path.join(output_dir, output_file)

encoding = {gws_grace.name: {"zlib": True, "complevel": 4}}
ds_out.to_netcdf(output_path, encoding=encoding)

print(f"Saved {output_file}")
