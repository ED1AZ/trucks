import geopandas as gpd

file = gpd.read_file("data/truck_volume.geojson")
#check columns
print(file.columns)