"""
Clean and standardize the Northwestern University ethnic media outlets dataset.

This script reads a CSV file containing ethnic media outlet data from Northwestern University,
standardizes the target community names using a predefined mapping, and outputs a cleaned CSV file.

The script expects two command line arguments:
1. Input file path: Path to the raw NWU ethnic media outlets CSV file
2. Output file path: Path where the cleaned CSV file should be saved

The cleaning process includes:
- Selecting only the domain and target_community columns
- Mapping target community names to standardized values:
    - "African American" -> "Black"
    - "Latino" -> "Hispanic"
    - "Native American" -> "Native American"
    - "Asian American" -> "Asian"
    - All others -> "Other"

Example:
    $ python clean_nwu.py input.csv output.csv
"""

import pandas as pd
import sys

nwu_ethnic_media_outlets_file = sys.argv[1]
output_file = sys.argv[-1]

raw_df = pd.read_csv(
    nwu_ethnic_media_outlets_file, usecols=["domain", "target_community"]
)


def clean_community(community: str) -> str:
    """
    Clean the community name to a standard format.
    Default to "Other" if the community is not in the mapping.

    Args:
        community (str): The community name to clean.

    Returns:
        str: The cleaned community name.
    """
    community_mapping = {
        "African American": "Black",
        "Latino": "Hispanic",
        "Native American": "Native American",
        "Asian American": "Asian",
    }
    return community_mapping.get(community, "Other")


raw_df["target_community"] = raw_df["target_community"].apply(clean_community)

raw_df.to_csv(output_file, index=False)
