import geopandas as gpd
import pystac_client
import planetary_computer
import rasterio
from rasterio.mask import mask
from rasterio.warp import transform_geom
import numpy as np
from datetime import datetime, timedelta

# Load boundary in native CRS
finca = gpd.read_file("finca.gpkg")
# Get bbox in WGS84 for STAC search
finca_wgs84 = finca.to_crs("epsg:4326")
bbox = finca_wgs84.total_bounds

dates_str = [
    "20240929", "20241022", "20241106", "20241221", "20250115",
    "20250216", "20250328", "20250425", "20250529", "20250629",
    "20250731", "20250830"
]

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)

def get_ndvi(target_date_str):
    target_date = datetime.strptime(target_date_str, "%Y%m%d")
    date_range = f"{(target_date - timedelta(days=7)).strftime('%Y-%m-%d')}/{(target_date + timedelta(days=7)).strftime('%Y-%m-%d')}"

    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=date_range,
        query={"eo:cloud_cover": {"lt": 20}}
    )

    items = list(search.items())
    if not items:
        print(f"No clear image found for {target_date_str}")
        return None

    items.sort(key=lambda x: abs(x.datetime.replace(tzinfo=None) - target_date))
    item = items[0]
    print(f"Using {item.id} for {target_date_str} (Cloud cover: {item.properties['eo:cloud_cover']:.2f}%)")

    # Reproject geometry to item CRS for masking
    with rasterio.open(item.assets["B04"].href) as red_src:
        item_crs = red_src.crs
        finca_item_crs = finca.to_crs(item_crs)

        red, out_transform = mask(red_src, finca_item_crs.geometry, crop=True)
        out_meta = red_src.meta.copy()

    with rasterio.open(item.assets["B08"].href) as nir_src:
        nir, _ = mask(nir_src, finca_item_crs.geometry, crop=True)

    red = red[0].astype(float)
    nir = nir[0].astype(float)
    ndvi = (nir - red) / (nir + red + 1e-10)

    out_meta.update({
        "driver": "GTiff",
        "height": red.shape[0],
        "width": red.shape[1],
        "transform": out_transform,
        "dtype": rasterio.float32,
        "count": 1,
        "nodata": -9999
    })

    output_fn = f"ndvi_{target_date_str}.tif"
    with rasterio.open(output_fn, "w", **out_meta) as dst:
        dst.write(ndvi.astype(rasterio.float32), 1)

    return output_fn

for d in dates_str:
    get_ndvi(d)
