import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

# decide overnight demand based on type of road (major = higher aadt, local = less aadt)
def overnight_factor(aadt):
    if aadt > 5000:
        return 0.45   # major freight corridors
    elif aadt > 1000:
        return 0.35
    else:
        return 0.25   # rural / local roads


def nearby_trucks(point, gdf_roads):
    SERVICE_RADIUS = 20000  
    
    buffer = point.buffer(SERVICE_RADIUS)
    nearby = gdf_roads[gdf_roads.intersects(buffer)].copy()

    # Distance decay
    nearby["dist"] = nearby.distance(point)
    nearby["weight"] = np.exp(-nearby["dist"] / 20000)

    # Assign overnight factor based on AADT
    nearby["overnight_factor"] = nearby["TruckAADT"].apply(overnight_factor)

    # Total demand
    nearby["weighted_demand"] = nearby["TruckAADT"] * nearby["weight"]

    # Overnight demand (
    nearby["overnight_weighted"] = (
        nearby["TruckAADT"] *
        nearby["weight"] *
        nearby["overnight_factor"]
    )

    return pd.Series({
        "truck_demand": nearby["weighted_demand"].sum(),
        "overnight_demand": nearby["overnight_weighted"].sum()
    })


# load data
gdf_parking = gpd.read_file("data/florida_stops.geojson")
gdf_roads = gpd.read_file("data/truck_volume.geojson")

#convert to meters for accurate distance calculations
gdf_parking = gdf_parking.to_crs(epsg=3857)
gdf_roads = gdf_roads.to_crs(epsg=3857)

# add truck demand and capacity gap columns
demand_results = gdf_parking.geometry.apply(
    nearby_trucks, args=(gdf_roads,)
)

gdf_parking[["truck_demand", "overnight_demand"]] = demand_results


# Capacity calculations
gdf_parking["capacity_gap"] = (
    gdf_parking["truck_demand"] - gdf_parking["number_of_spots"]
)

gdf_parking["overnight_gap"] = (
    gdf_parking["overnight_demand"] - gdf_parking["number_of_spots"]
)

# identify problems
overloaded = gdf_parking[gdf_parking["capacity_gap"] > 0]
underused = gdf_parking[gdf_parking["capacity_gap"] < 0]

def nearest_parking_distance(line):
    return gdf_parking.distance(line).min()


# Summary messages
print("Total truck demand served:", gdf_parking["truck_demand"].sum())
print("Number of overloaded facilities:", len(overloaded))

print("\nOverloaded facilities by county:")
overloaded_counties = overloaded.groupby("county")["capacity_gap"].sum().sort_values(ascending=False)
print(overloaded_counties)

# Bar Graphs
plt.figure(figsize=(10,6))
overloaded_counties.plot(kind="bar", color="red")
#plt.title("Total Positive Capacity Gap by County (Overloaded)")
plt.ylabel("Capacity Gap (in millions of trucks)")
plt.xlabel("County")
plt.tight_layout()
plt.savefig("overloaded_counties.png")
plt.show()


# RURAL COUNTIES THAT ARE OVERLOADED
rural_counties = [
    "Monroe", "Hendry", "Glades", "Okeechobee", "Highlands", "DeSoto",
    "Hardee", "Washington", "Walton", "Holmes", "Jackson", "Calhoun",
    "Gulf", "Liberty", "Franklin", "Gadsden", "Wakulla", "Jefferson",
    "Taylor", "Madison", "Hamilton", "Suwannee", "Lafayette", "Dixie",
    "Levy", "Gilchrist", "Columbia", "Baker", "Union", "Bradford"
]
rural_overloaded = overloaded[
    overloaded["county"].isin(rural_counties)
]

rural_overloaded_counties = (
    rural_overloaded.groupby("county")["capacity_gap"]
    .sum()
    .sort_values(ascending=False)
)
plt.figure(figsize=(10,6))
rural_overloaded_counties.plot(kind="bar", color="green")
plt.ylabel("Capacity Gap")
plt.xlabel("Rural County")
plt.tight_layout()
plt.savefig("rural_overloaded_counties.png")
plt.show()


# OVERNIGHT DEMANDS BY COUNTY
overnight_counties = (
    gdf_parking.groupby("county")["overnight_demand"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10,6))
overnight_counties.plot(kind="bar")
plt.ylabel("Overnight Demand")
plt.xlabel("County")
plt.tight_layout()
plt.savefig("overnight_demand_counties.png")
plt.show()


# Summary Table
summary_df = gdf_parking[["county", "truck_demand", "number_of_spots", "capacity_gap"]]
summary_df = summary_df.groupby("county").sum().reset_index()
print(summary_df)
