#%%
import ast

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def parse_seq(col):
    return col.apply(ast.literal_eval)

FE_TYPE = "darkflow"
files_stage1 = [
    f"google.com-1/{FE_TYPE}-stage1_raw.csv",
    f"google.com-2/{FE_TYPE}-stage1_raw.csv",
    f"google.com-3/{FE_TYPE}-stage1_raw.csv"
]
dfs_stage1 = []
for i, f in enumerate(files_stage1, 1):
    df = pd.read_csv(f)
    df["batch"] = i
    df["stage"] = "stage1"
    dfs_stage1.append(df)
df_stage1 = pd.concat(dfs_stage1, ignore_index=True)


files_stage2 = [
    f"google.com-1/{FE_TYPE}-stage2_tor.csv",
    f"google.com-2/{FE_TYPE}-stage2_tor.csv",
    f"google.com-3/{FE_TYPE}-stage2_tor.csv"
]
dfs_stage2 = []
for i, f in enumerate(files_stage2, 1):
    df = pd.read_csv(f)
    df["batch"] = i
    df["stage"] = "stage2"
    dfs_stage2.append(df)
df_stage2 = pd.concat(dfs_stage2, ignore_index=True)

files_stage3 = [
    f"google.com-1/{FE_TYPE}-stage3_clash.csv",
    f"google.com-2/{FE_TYPE}-stage3_clash.csv",
    f"google.com-3/{FE_TYPE}-stage3_clash.csv"
]
dfs_stage3 = []
for i, f in enumerate(files_stage3, 1):
    df = pd.read_csv(f)
    df["batch"] = i
    df["stage"] = "stage3"
    dfs_stage3.append(df)
df_stage3 = pd.concat(dfs_stage3, ignore_index=True)

df_all = pd.concat([df_stage1, df_stage2, df_stage3], ignore_index=True)

# %%
df_all.columns = (
    df_all.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
    .str.replace('.', '')
)
df_all["pkt_dir_seq"] = parse_seq(df_all["pkt_dir_seq"])
df_all["pkt_len_seq"] = parse_seq(df_all["pkt_len_seq"])
df_all["pkt_usec_seq"] = parse_seq(df_all["pkt_usec_seq"])

#%%
row = df.iloc[0]

plt.figure(figsize=(10,2))
plt.plot(row["pkt_dir_seq"], marker='o')
plt.title("Packet Direction Sequence")
plt.yticks([-1,1])
plt.show()
