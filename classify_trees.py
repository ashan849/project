import rasterio
import numpy as np
import glob

# Identify trees based on high NDVI in spring (20250425)
spring_ndvi_fn = "ndvi_20250425.tif"

with rasterio.open(spring_ndvi_fn) as src:
    ndvi = src.read(1)
    # Threshold for trees (heuristic: pixels with NDVI > 0.35 in spring are likely trees/shrubs in this semi-arid region)
    # Actually, looking at the range [0.0, 0.5288], 0.35 seems reasonable.
    tree_mask = (ndvi > 0.35).astype(np.uint8)

    meta = src.meta.copy()
    meta.update(dtype=rasterio.uint8, nodata=0)

    with rasterio.open("tree_mask.tif", "w", **meta) as dst:
        dst.write(tree_mask, 1)

# Generate grass pixel layer (binary)
grass_mask = (ndvi <= 0.35) & (ndvi > 0.05) # excluding non-vegetated/bare soil and trees
grass_mask = grass_mask.astype(np.uint8)

with rasterio.open("grass_mask.tif", "w", **meta) as dst:
    dst.write(grass_mask, 1)

print("Tree and Grass masks generated.")
