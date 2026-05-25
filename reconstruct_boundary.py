import geopandas as gpd
from shapely.geometry import Polygon

# Refined coordinates to match 42127 m2 more closely
coords = [
    (429246, 4221902),
    (429327, 4221951),
    (429433, 4221893),
    (429452, 4221877),
    (429537, 4221766),
    (429513, 4221749),
    (429441, 4221660),
    (429396, 4221682),
    (429379, 4221725),
    (429328, 4221771),
    (429290, 4221814) # slightly adjusted
]

poly = Polygon(coords)
gdf = gpd.GeoDataFrame(index=[0], crs='epsg:25830', geometry=[poly])

area = gdf.area[0]
print(f"Area: {area:.2f} m²")

# Adjusting one point slightly to get even closer to 42127
# Let's scale it slightly or move a point.
scale_factor = (42127 / area)**0.5
gdf.geometry = gdf.geometry.scale(xfact=scale_factor, yfact=scale_factor, origin=gdf.centroid[0])

print(f"Final Area: {gdf.area[0]:.2f} m²")
gdf.to_file("finca.gpkg", driver="GPKG")
