#%%
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


FE_TYPE = "nfstream"
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
cols_to_drop = [
    "flow_id",
    "src_ip",
    "dst_ip",
    "timestamp"
]

X = df_all.drop(columns=cols_to_drop, errors="ignore")
X.columns = X.columns.str.replace('/', '_per_')

numeric_cols = X.select_dtypes(include=[np.number]).columns
X[numeric_cols] = np.log1p(X[numeric_cols])

#%%
labels = df_all["stage"]
X = df_all.select_dtypes(include=[np.number])
X = X.drop(columns=["batch", "src_port", "dst_port", "protocol"], errors="ignore")

X = X.fillna(0)
X_scaled = StandardScaler().fit_transform(X)

# %%
X_2d = PCA(n_components=2).fit_transform(X_scaled)

plt.figure(figsize=(6,5))

for stage in labels.unique():
    idx = labels == stage
    plt.scatter(X_2d[idx,0], X_2d[idx,1], s=10, label=stage)

plt.legend()
plt.title("PCA by Stage")
plt.show()

# %%
from sklearn.manifold import TSNE

tsne = TSNE(
    n_components=2,
    perplexity=5,
    random_state=42,
    max_iter=1000
)
X_tsne = tsne.fit_transform(X_scaled)

plt.figure(figsize=(7,6))

for stage in labels.unique():
    idx = labels == stage
    plt.scatter(
        X_tsne[idx, 0],
        X_tsne[idx, 1],
        s=10,
        label=stage
    )

plt.legend()
plt.title("t-SNE: Flow Distribution by Stage")
plt.xlabel("Dim 1")
plt.ylabel("Dim 2")
plt.show()
# %%
