import pandas as pd
import sys

input_files = sys.argv[1:-1]
output_file = sys.argv[-1]

columns_to_keep = [
    "domain",
    "target_community",
    "dataset",
]

dfs = []
for file in input_files:
    df = pd.read_csv(file, usecols=columns_to_keep)
    dfs.append(df)

df = pd.concat(dfs)
df.to_csv(output_file, index=False)
