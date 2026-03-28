import pandas as pd

df = pd.read_csv("data/florida_stops.csv")

rural_counties = {
    "Monroe", "Hendry", "Glades", "Okeechobee", "Glades", "Highlands", "DeSoto", "Hardee", "Washington", "Walton", "Holmes", "Jackson", "Calhoun", "Gulf", "Liberty", "Franklin", "Gadsden", "Wakulla", "Jefferson", "Taylor", "Madison", "Hamilton", "Suwannee", "Lafayette", "Dixie", "Levy", "Gilchrist", "Columbia", "Baker", "Union", "Bradford"
}
# Rural Counties: Monroe, Hendry, Glades, Okeechobee, Glades, Highlands, DeSoto, Hardee, Washington, Walton, Holmes, Jackson, Calhoun, Gulf, Liberty, Franklin, Gadsden, Wakulla, Jefferson, Taylor, Madison, Hamilton, Suwannee, Lafayette, Dixie, Levy, Gilchrist, Columbia, Baker, Union, Bradford

# Filter for rural counties
rural_stops = df[df["county"].isin(rural_counties)]

# Count stops by county
county_counts = rural_stops["county"].value_counts().sort_values(ascending=False)

print("Stops at each rural county:")
print(county_counts)
print(f"\nTotal stops in rural counties: {len(rural_stops)}")

# Filter for non-rural counties
non_rural_stops = df[~df["county"].isin(rural_counties)]

# Count stops by non-rural county
non_rural_counts = non_rural_stops["county"].value_counts().sort_values(ascending=False)

print("\nStops at each non-rural county:")
print(non_rural_counts)
print(f"\nTotal stops in non-rural counties: {len(non_rural_stops)}")
