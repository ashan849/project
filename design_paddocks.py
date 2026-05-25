import geopandas as gpd
from shapely.geometry import box, LineString
from shapely.ops import split
import numpy as np

finca = gpd.read_file("finca.gpkg")
poly = finca.geometry[0]
minx, miny, maxx, maxy = poly.bounds

# Let's use vertical lines to split
x_range = maxx - minx
# We want roughly equal areas. Since it's wider in the middle, we need to find the correct x values.
def find_split_x(target_area, start_x, end_x, poly):
    # simple binary search
    for _ in range(20):
        mid_x = (start_x + end_x) / 2
        test_box = box(minx, miny - 100, mid_x, maxy + 100)
        area = poly.intersection(test_box).area
        if area < target_area:
            start_x = mid_x
        else:
            end_x = mid_x
    return mid_x

total_area = poly.area
target = total_area / 3

x1 = find_split_x(target, minx, maxx, poly)
x2 = find_split_x(2 * target, minx, maxx, poly)

parts = []
parts.append(poly.intersection(box(minx, miny-100, x1, maxy+100)))
parts.append(poly.intersection(box(x1, miny-100, x2, maxy+100)))
parts.append(poly.intersection(box(x2, miny-100, maxx, maxy+100)))

gdf_subs = gpd.GeoDataFrame({
    'id': [1, 2, 3],
    'nombre': ['C1', 'C2', 'C3']
}, crs='epsg:25830', geometry=parts)

print(f"Subdivision areas: {[p.area/10000 for p in parts]} ha")
gdf_subs.to_file("subdivisions.gpkg", driver="GPKG")
