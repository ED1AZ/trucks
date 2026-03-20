import pandas as pd

df = pd.read_csv("data/truck_stop_parking.csv")

# Florida ID = 12
filtered_df = df[df["state_number"] == 12]
    
# Write the filtered df to a new CSV file
path = "florida_stops.csv"
filtered_df.to_csv(path, index=False)
print(f"Filtered data saved to {path}")