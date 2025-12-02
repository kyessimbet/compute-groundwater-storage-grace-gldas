Computation of Groundwater Storage Anomalies from GRACE and GLDAS by Kamilya Yessimbet

These scripts implement the total water balance approach to estimate groundwater storage anomalies by combining GRACE satellite gravimetry with GLDAS land surface model outputs. 
The workflow isolates groundwater variability by subtracting soil moisture, snow, and surface water contributions from GRACE total water storage.

The repository provides tools to:

- Load and preprocess GRACE and GLDAS datasets
- Ensure spatial and temporal compatibility between the two sources
- Compute groundwater storage anomalies across the overlapping 2002–2024 record
- Save results in NetCDF format for further hydrological analysis or visualization
