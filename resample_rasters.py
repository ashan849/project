import rasterio
from rasterio.enums import Resampling
import numpy as np
import glob
import os

def resample_raster(input_path, output_path, upscale_factor=5):
    with rasterio.open(input_path) as dataset:
        # resample data to target shape
        data = dataset.read(
            out_shape=(
                dataset.count,
                int(dataset.height * upscale_factor),
                int(dataset.width * upscale_factor)
            ),
            resampling=Resampling.bilinear
        )

        # scale image transform
        transform = dataset.transform * dataset.transform.scale(
            (dataset.width / data.shape[-1]),
            (dataset.height / data.shape[-2])
        )

        profile = dataset.profile.copy()
        profile.update({
            'transform': transform,
            'width': data.shape[-1],
            'height': data.shape[-2]
        })

        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(data)

# Resample from 10m to 2m (factor of 5)
os.makedirs("rasters_2m", exist_ok=True)
rasters_to_resample = ["slope_25830.tif", "distance_to_water.tif", "grass_mask.tif", "tree_mask.tif"] + glob.glob("ndvi_*.tif")

for r in rasters_to_resample:
    out_name = os.path.join("rasters_2m", os.path.basename(r))
    resample_raster(r, out_name, upscale_factor=5)
    print(f"Resampled {r} to 2m")
