import pandas as pd
import sys
from url_utils import extract_domain, remove_parameters, extract_path

cuny_black_media_list_file = sys.argv[1]
output_file = sys.argv[-1]

raw_df = pd.read_csv(
    cuny_black_media_list_file,
    usecols=[
        "Name of publication",
        "Delivery",
        "State",
        "URL",
        "Audience",
        "Audience: City/region",
    ],
)
print(f"Loaded {len(raw_df)} rows")

# Rename columns
raw_df.rename(
    columns={
        "Name of publication": "media_name",
        "Delivery": "primary_format",
        "State": "state",
        "URL": "website",
        "Audience": "primary_community_served",
        "Audience: City/region": "primary_community_served_city_region",
    },
    inplace=True,
)

# Only keep the ones with website
raw_df = raw_df[raw_df["website"].notna()]
print(f"After filtering, {len(raw_df)} rows remain")

# Process the URLs
raw_df["url"] = raw_df.website.apply(remove_parameters)
raw_df["domain"] = raw_df.url.apply(extract_domain)
# Extract the path
raw_df["path"] = raw_df.url.apply(extract_path)

# Remove cases where domains is not valid
raw_df = raw_df[raw_df.domain != ""].copy()

# Remove duplicates
raw_df = raw_df.drop_duplicates(subset=["domain", "path"])
print(f"Number of unique domains and paths: {len(raw_df)}")

raw_df.to_csv(output_file, index=False)

# Many local news outlets' websites are hosted as sections of a larger website.
# Since it's difficult to track those websites, we will mainly focus on the outlets with a top-level domains.
# This is done by:
# 1. Finding URLs with no path
# 2. For those with a path, focus on the ones with path=\news or \about

# 1. Finding URLs with no path
no_path_df = raw_df[raw_df["path"] == ""]
print(f"Number of black media sites with no path: {len(no_path_df)}")

# 2. For those with a path, focus on the ones with path=\news or \about
path_df = raw_df[raw_df["path"] != ""].copy()
print(f"Number of black media sites with a path: {len(path_df)}")


def is_ethnic_media_site(path):
    cleaned_path = path.strip("/")
    path_set = {
        "news",
        "site",
        "about",
        "index.html",
        "index.php",
        "articles",
        "en",
        "content",
    }
    return cleaned_path in path_set


path_df["is_ethnic_media_site"] = path_df["path"].apply(is_ethnic_media_site)
path_df = path_df[path_df["is_ethnic_media_site"]]
print(
    f"Number of ethnic media sites with a path that contains 'news', 'home', 'about', 'index.html', or 'index.php': {len(path_df)}"
)

ethnic_media_df = pd.concat([no_path_df, path_df])
print(f"Number of ethnic media sites: {len(ethnic_media_df)}")

ethnic_media_df.drop_duplicates(subset=["domain"], inplace=True)
print(f"Number of ethnic media sites after removing duplicates: {len(ethnic_media_df)}")

# Add target_community
ethnic_media_df["target_community"] = "Black"
ethnic_media_df["dataset"] = "cuny_black"


cols_to_keep = [
    "media_name",
    "primary_format",
    "domain",
    "target_community",
    "primary_community_served",
    "primary_community_served_city_region",
    "state",
    "dataset",
]
ethnic_media_df[cols_to_keep].to_csv(output_file, index=False)
