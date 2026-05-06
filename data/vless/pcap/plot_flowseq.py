# %%
import ast
from itertools import zip_longest

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns


def parse_seq(col):
    return col.apply(ast.literal_eval)


WEBSITE = "github.com"
FE_TYPE = "darkflow"
files_stage1 = [
    f"{WEBSITE}-1/{FE_TYPE}-stage1_raw.csv",
    f"{WEBSITE}-2/{FE_TYPE}-stage1_raw.csv",
    f"{WEBSITE}-3/{FE_TYPE}-stage1_raw.csv"
]
dfs_stage1 = []
for i, f in enumerate(files_stage1, 1):
    df = pd.read_csv(f)
    df["batch"] = i
    df["stage"] = "stage1"
    dfs_stage1.append(df)
df_stage1 = pd.concat(dfs_stage1, ignore_index=True)


files_stage2 = [
    f"{WEBSITE}-1/{FE_TYPE}-stage2_tor.csv",
    f"{WEBSITE}-2/{FE_TYPE}-stage2_tor.csv",
    f"{WEBSITE}-3/{FE_TYPE}-stage2_tor.csv"
]
dfs_stage2 = []
for i, f in enumerate(files_stage2, 1):
    df = pd.read_csv(f)
    df["batch"] = i
    df["stage"] = "stage2"
    dfs_stage2.append(df)
df_stage2 = pd.concat(dfs_stage2, ignore_index=True)

files_stage3 = [
    f"{WEBSITE}-1/{FE_TYPE}-stage3_clash.csv",
    f"{WEBSITE}-2/{FE_TYPE}-stage3_clash.csv",
    f"{WEBSITE}-3/{FE_TYPE}-stage3_clash.csv"
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


# %%
row = df_all.iloc[0]

plt.figure(figsize=(10,2))
plt.plot(row["pkt_dir_seq"], marker='o')
plt.title("Packet Direction Sequence")
plt.yticks([-1,1])
plt.show()


# %%
plt.figure(figsize=(10,3))
plt.plot(row["pkt_len_seq"], marker='o')
plt.title("Packet Length Sequence")
plt.ylabel("Bytes")
plt.show()


# %%
ts = np.array(row["pkt_usec_seq"])
iat = np.diff(ts)

plt.figure(figsize=(10,3))
plt.plot(iat, marker='o')
plt.title("Inter-Arrival Time (usec)")
plt.show()


# %%
fig, axs = plt.subplots(3, 1, figsize=(10,6), sharex=True)

axs[0].plot(row["pkt_dir_seq"])
axs[0].set_title("Direction")

axs[1].plot(row["pkt_len_seq"])
axs[1].set_title("Length")

axs[2].plot(iat)
axs[2].set_title("IAT")

plt.tight_layout()
plt.show()


# %%
for i in range(5):
    row = df_all.iloc[i]
    plt.plot(row["pkt_len_seq"], alpha=0.3)

plt.title("Packet Length Overlay")
plt.show()


# %%
# MARK
def pad_sequences(seqs, max_len=100):
    padded = [
        list(seq[:max_len]) + [0]*(max_len-len(seq))
        if len(seq)<max_len else seq[:max_len]
        for seq in seqs
    ]
    return np.array(padded)

X_len = pad_sequences(df_all["pkt_len_seq"], max_len=100)

plt.figure(figsize=(10,5))
sns.heatmap(X_len, cmap="viridis")
plt.title("Packet Length Heatmap")
plt.xlabel("Packet Index")
plt.ylabel("Flow")
plt.show()


# %%
for stage in df_all["stage"].unique():
    df_stage = df_all[df_all["stage"] == stage]

    X_len = pad_sequences(df_stage["pkt_len_seq"], max_len=100)

    plt.figure(figsize=(10,4))
    sns.heatmap(X_len, cmap="viridis")
    plt.title(f"Packet Length Heatmap - {stage}")
    plt.xlabel("Packet Index")
    plt.ylabel("Flow")
    plt.show()


# %%
stages = df_all["stage"].unique()

fig, axes = plt.subplots(1, len(stages), figsize=(15,4), sharey=True)

for i, stage in enumerate(stages):
    df_stage = df_all[df_all["stage"] == stage]
    X_len = pad_sequences(df_stage["pkt_len_seq"], max_len=100)

    sns.heatmap(X_len, cmap="viridis", ax=axes[i], cbar=False)
    axes[i].set_title(stage)
    axes[i].set_xlabel("Packet Index")

axes[0].set_ylabel("Flow")

plt.suptitle("Packet Length Comparison by Stage")
plt.tight_layout()
plt.show()


# %%
def combine_dir_len(row):
    return [d*l for d,l in zip(row["pkt_dir_seq"], row["pkt_len_seq"])]

df_all["signed_len_seq"] = df_all.apply(combine_dir_len, axis=1)

row = df_all.iloc[8]

plt.figure(figsize=(10,3))
plt.plot(row["signed_len_seq"])
plt.title("Signed Packet Length Sequence")
plt.axhline(0, color='black')
plt.show()


# %%
