Computation of Groundwater Storage Anomalies from GRACE and GLDAS by Kamilya Yessimbet

These scripts implement the total water balance approach to estimate groundwater storage anomalies by combining GRACE satellite gravimetry with GLDAS land surface model outputs. 
The workflow isolates groundwater variability by subtracting soil moisture, snow, and surface water contributions from GRACE total water storage.

This repository provides analysis for processing GRACE and GLDAS datasets and generating groundwater storage anomaly products suitable for hydrological analysis.

1) GRACE & GLDAS Preprocessing

* Extracts a reference latitude–longitude grid from GLDAS NetCDF files and saves it as a CSV.

* Interpolates GRACE data onto this reference grid.

* Synchronizes GLDAS NetCDF files with GRACE reference timestamps.

2) Soil Moisture Aggregation

Computes total (0–200 cm) soil moisture from GLDAS by combining individual soil-layer variables.

3) Groundwater Storage Anomalies

Calculates groundwater storage anomalies over the overlapping 2002–2024 GRACE–GLDAS period.

4) Standardized Output

Saves all processed data products in NetCDF format, ready for hydrological research, visualization, or modeling workflows.
