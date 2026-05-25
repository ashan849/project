import geopandas as gpd
import pystac_client
import planetary_computer
import rasterio
from rasterio.mask import mask
import numpy as np
from rasterio.warp import calculate_default_transform, reproject, Resampling

# Load boundary
finca = gpd.read_file("finca.gpkg").to_crs("epsg:4326")
# Buffer slightly to ensure we have enough pixels for gradient at edges
finca_buffered = finca.buffer(0.001).to_crs("epsg:4326")
bbox = finca_buffered.total_bounds

# Search for DEM
catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)

search = catalog.search(
    collections=["cop-dem-glo-30"],
    bbox=bbox,
)

items = list(search.items())
dem_url = items[0].assets["data"].href

with rasterio.open(dem_url) as src:
    out_image, out_transform = mask(src, finca_buffered.geometry, crop=True)
    out_meta = src.meta.copy()

out_meta.update({
    "driver": "GTiff",
    "height": out_image.shape[1],
    "width": out_image.shape[2],
    "transform": out_transform,
    "crs": "epsg:4326"
})

with rasterio.open("dem_temp.tif", "w", **out_meta) as dest:
    dest.write(out_image)

# Reproject to EPSG:25830
dst_crs = 'EPSG:25830'
# Target 10m resolution to match Sentinel-2
dst_res = 10.0

with rasterio.open("dem_temp.tif") as src:
    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds, resolution=dst_res)
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height,
        'nodata': -9999
    })

    with rasterio.open("dem_25830.tif", 'w', **kwargs) as dst:
        reproject(
            source=rasterio.band(src, 1),
            destination=rasterio.band(dst, 1),
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear)

# Calculate Slope using 10m resolution
with rasterio.open("dem_25830.tif") as src:
    data = src.read(1).astype(float)
    data[data == -9999] = np.nan
    res = src.res[0]

    # Simple 4-neighbor slope
    x, y = np.gradient(data, res)
    slope = np.arctan(np.sqrt(x**2 + y**2)) * (180 / np.pi)

    meta = src.meta.copy()
    meta.update(dtype=rasterio.float32, nodata=np.nan)
    with rasterio.open("slope_25830.tif", "w", **meta) as dst:
        dst.write(slope.astype(rasterio.float32), 1)

print("DEM and Slope processing complete at 10m resolution.")
