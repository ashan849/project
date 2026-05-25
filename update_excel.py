import pandas as pd
import numpy as np
import rasterio
import geopandas as gpd
from rasterstats import gen_zonal_stats
import glob

# Load subdivisions and masks
subs = gpd.read_file("subdivisions.gpkg")
with rasterio.open("grass_mask.tif") as src:
    grass_mask = src.read(1)
    affine = src.transform

# We need pixel-level data as requested (but Excel usually expects a row per subdivision or similar)
# Client's Excel has "id", "area", "pendiente", "distancia", and 12 NDVI columns.
# It seems each row in the NDVI sheet represents a pixel or a sample.
# Given it has 10,747 rows for 4.21 ha, that's roughly 2552 pixels per hectare.
# A 2m resolution pixel is 4 m2. 10000 / 4 = 2500 pixels.
# Our rasters are at 10m (100 m2), so we'll have fewer rows if we use pixels.
# Let's resample or just use the 10m pixels.
# 42127 m2 / 100 m2 = ~421 pixels.

# To be professional and match the "feel" of the original Excel,
# I will generate rows for each 10m pixel that is 'grass'.

def extract_pixel_data():
    rows = []

    # Load all NDVI rasters
    ndvi_files = sorted(glob.glob("ndvi_*.tif"))
    ndvi_data = {}
    for f in ndvi_files:
        date_str = f.split("_")[1].split(".")[0]
        with rasterio.open(f) as src:
            ndvi_data[date_str] = src.read(1)

    with rasterio.open("slope_25830.tif") as src:
        slope_data = src.read(1)
    with rasterio.open("distance_to_water.tif") as src:
        dist_data = src.read(1)
    with rasterio.open("grass_mask.tif") as src:
        grass_data = src.read(1)
        affine = src.transform

    for r in range(grass_data.shape[0]):
        for c in range(grass_data.shape[1]):
            if grass_data[r, c] == 1:
                # Get coordinates
                x, y = affine * (c + 0.5, r + 0.5)
                point = gpd.points_from_xy([x], [y])[0]

                # Find which subdivision
                sub_id = np.nan
                for idx, sub in subs.iterrows():
                    if sub.geometry.contains(point):
                        sub_id = sub['id']
                        break

                if np.isnan(sub_id): continue

                pixel_row = {
                    'id': sub_id,
                    'area': 0.01, # 100 m2 = 0.01 ha
                    'pendiente': slope_data[r, c],
                    'distancia': dist_data[r, c]
                }

                for date_str, data in ndvi_data.items():
                    pixel_row[f"{date_str} NDVI"] = data[r, c]

                rows.append(pixel_row)

    return pd.DataFrame(rows)

df_new_ndvi = extract_pixel_data()

# Read original Excel to keep structure
orig_xlsx = pd.ExcelFile('Plan de pastoreo.xlsx')
sheets = {name: orig_xlsx.parse(name) for name in orig_xlsx.sheet_names}

# Update NDVI sheet
sheets['NDVI'] = df_new_ndvi

# Save to new file first to verify
with pd.ExcelWriter('Plan de pastoreo_updated.xlsx', engine='openpyxl') as writer:
    for name, df in sheets.items():
        df.to_excel(writer, sheet_name=name, index=False)

print("Excel updated with 3-section pixel data.")
