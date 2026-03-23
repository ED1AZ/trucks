import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# Read the truck_stops CSV file and create a GeoDataFrame
df = pd.read_csv("data/florida_stops.csv")
geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)
gdf.set_crs("EPSG:4326", inplace=True)
gdf.to_file("data/florida_stops.geojson", driver="GeoJSON")