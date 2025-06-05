import pandas as pd
import sys

raw_data_file = sys.argv[1]
final_data_file = sys.argv[2]

raw_df = pd.read_csv(raw_data_file)
print(f"Loaded {len(raw_df)} rows")

# Only keep domains serving certain communities
target_communities = ["Asian", "Black", "Hispanic"]

raw_df = raw_df[raw_df["target_community"].isin(target_communities)]
print(f"Filtered to {len(raw_df)} rows after filtering by community")

# Remove the domains with inconsistent target communities
target_community_counts = raw_df.groupby("domain")["target_community"].nunique()
raw_df = raw_df[
    raw_df["domain"].isin(target_community_counts[target_community_counts == 1].index)
]
print(f"Filtered to {len(raw_df)} rows after filtering by domain")

raw_df = raw_df.drop_duplicates(subset=["domain"])
print(f"Filtered to {len(raw_df)} rows after dropping duplicates")

columns_to_keep = [
    "domain",
    "target_community",
]
raw_df[columns_to_keep].to_csv(final_data_file, index=False)
