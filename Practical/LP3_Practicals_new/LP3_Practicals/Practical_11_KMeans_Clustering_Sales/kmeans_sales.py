# %% [markdown]
# # Practical 11 : K-Means and Hierarchical Clustering on sales_data_sample.csv
# Group the sales orders into clusters and find the best number of clusters with the **Elbow method**.
#
# Dataset: `sales_data_sample.csv` (Kaggle - kyanyoga/sample-sales-data), kept in this folder.
# Note: the file is **latin-1 encoded**, so it is read with `encoding="latin1"`.

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage

# %% [markdown]
# ## 1. Load and inspect the dataset

# %%
df = pd.read_csv("sales_data_sample.csv", encoding="latin1")
print("Shape:", df.shape)
print(df.head())
df.info()

# %% [markdown]
# ## 2. Pre-processing / feature selection
# Clustering needs numeric features. Identifiers (ORDERNUMBER), dates, names, addresses and phone
# numbers say nothing about *buying behaviour*, so they are dropped.
# Features kept: **QUANTITYORDERED, PRICEEACH, SALES, MSRP**. `DEALSIZE` (Small/Medium/Large) is kept
# separately to check the clusters afterwards.

# %%
features = ["QUANTITYORDERED", "PRICEEACH", "SALES", "MSRP"]
data = df[features].dropna()
print(data.describe().T)

# K-Means uses Euclidean distance, so scale the features (SALES is in thousands, QUANTITY in tens)
scaler = StandardScaler()
X = scaler.fit_transform(data)

# %% [markdown]
# ## 3. Elbow method: find the number of clusters
# **WCSS / inertia** = sum of squared distances of each point to its cluster centre.
# It always drops as k grows. The "elbow" is the k after which the drop becomes small.
# Adding more clusters beyond that gives little benefit.

# %%
wcss = []
k_range = range(1, 11)
for k in k_range:
    km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
    km.fit(X)
    wcss.append(km.inertia_)

plt.figure(figsize=(8, 4))
plt.plot(list(k_range), wcss, marker="o")
plt.xlabel("Number of clusters (k)")
plt.ylabel("WCSS (inertia)")
plt.title("Elbow method")
plt.xticks(list(k_range))
plt.show()

for k, w in zip(k_range, wcss):
    print(f"k={k:2d}  WCSS={w:10.2f}")

# Silhouette score as a second check (closer to 1 = better separated clusters)
for k in range(2, 7):
    labels = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X)
    print(f"k={k}  silhouette={silhouette_score(X, labels):.3f}")

# %% [markdown]
# ## 4. Apply K-Means with the chosen k
# The elbow appears at **k = 3**, which also matches the three deal sizes (Small / Medium / Large).

# %%
k_opt = 3
kmeans = KMeans(n_clusters=k_opt, init="k-means++", n_init=10, random_state=42)
data = data.copy()
data["Cluster"] = kmeans.fit_predict(X)

print("Cluster sizes:\n", data["Cluster"].value_counts().sort_index())
print("\nAverage values per cluster:\n", data.groupby("Cluster")[features].mean().round(2))
print("\nCluster vs actual DEALSIZE:\n", pd.crosstab(data["Cluster"], df.loc[data.index, "DEALSIZE"]))

centers = scaler.inverse_transform(kmeans.cluster_centers_)
plt.figure(figsize=(8, 5))
sns.scatterplot(x="QUANTITYORDERED", y="SALES", hue="Cluster", data=data, palette="Set1", s=25)
plt.scatter(centers[:, 0], centers[:, 2], c="black", s=200, marker="X", label="Centroids")
plt.title("K-Means clusters (Quantity vs Sales)")
plt.legend()
plt.show()

# %% [markdown]
# ## 5. Hierarchical (Agglomerative) clustering
# Starts with every point as its own cluster and repeatedly merges the two closest clusters
# (**Ward linkage** minimises the increase in variance). The **dendrogram** shows the merge tree;
# cutting it with a horizontal line at the biggest vertical gap gives the number of clusters.

# %%
Z = linkage(X, method="ward")
plt.figure(figsize=(12, 5))
dendrogram(Z, truncate_mode="lastp", p=30)
plt.title("Dendrogram (Ward linkage)")
plt.xlabel("Cluster (size)")
plt.ylabel("Distance")
plt.show()

agg = AgglomerativeClustering(n_clusters=k_opt, linkage="ward")
data["HCluster"] = agg.fit_predict(X)
print("Hierarchical cluster sizes:\n", data["HCluster"].value_counts().sort_index())
print("\nAverage values per hierarchical cluster:\n", data.groupby("HCluster")[features].mean().round(2))
