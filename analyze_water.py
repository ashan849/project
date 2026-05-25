import rasterio
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from scipy.ndimage import distance_transform_edt

# Load boundary and grass mask to find a logical water point
# Usually water is at a corner or near an entrance.
# Looking at the boundary, maybe near the lowest point or a road.
finca = gpd.read_file("finca.gpkg")
centroid = finca.centroid[0]

# Propose water point at the west side (likely access point)
water_point = Point(429250, 4221800)
water_gdf = gpd.GeoDataFrame(index=[0], crs='epsg:25830', geometry=[water_point])
water_gdf.to_file("proposed_water.gpkg", driver="GPKG")

with rasterio.open("grass_mask.tif") as src:
    res = src.res[0]
    transform = src.transform
    width = src.width
    height = src.height

    # Create distance raster
    # Pixel coordinates of water point
    row, col = src.index(water_point.x, water_point.y)

    dist_raster = np.zeros((height, width))
    # We can use a simple Euclidean distance from (row, col)
    rows, cols = np.indices(dist_raster.shape)
    dist_raster = np.sqrt(((rows - row) * res)**2 + ((cols - col) * res)**2)

    meta = src.meta.copy()
    meta.update(dtype=rasterio.float32, nodata=-9999)

    with rasterio.open("distance_to_water.tif", "w", **meta) as dst:
        dst.write(dist_raster.astype(rasterio.float32), 1)

print("Distance to water analysis complete.")
