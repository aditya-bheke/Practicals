# Practical 11 – K-Means / Hierarchical Clustering on Sales Data

**Aim:** Implement K-Means clustering and hierarchical clustering on `sales_data_sample.csv`. Determine the number of clusters using the elbow method.

## Files
| File | Purpose |
|---|---|
| `kmeans_sales.py` | Plain Python script |
| `kmeans_sales.ipynb` | Same code as a Jupyter notebook |
| `sales_data_sample.csv` | 2823 sales orders, 25 columns ([Kaggle source](https://www.kaggle.com/datasets/kyanyoga/sample-sales-data)) |

> Note: the theory section of the manual shows code for a *Mall Customers* dataset (Age, Income, Spending Score), but the assignment title asks for **sales_data_sample.csv**, so this code uses the sales dataset. The method is exactly the same.

## Setup and run
Do the one-time setup in the main `README.md` first. Then:
```bash
cd Practical_11_KMeans_Clustering_Sales
python kmeans_sales.py
# or
jupyter notebook kmeans_sales.ipynb
```
The CSV is **latin-1 encoded**, so the code uses `pd.read_csv(..., encoding="latin1")`. Without it you'd get a `UnicodeDecodeError`.

## Input guide
This program needs **no keyboard input**. It reads the CSV file in this folder automatically. Just run it from inside this folder.
When run as a `.py` script, each graph opens in its own window, and the program **continues only after you close that window**.

## Results obtained
| k | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| WCSS | 11292 | 6742 | **4766** | 3935 | 3348 | 2859 |

The drop is large from 1→2 (4550) and 2→3 (1976), then flattens (831, 586, …). The **elbow is at k = 3**. The three clusters roughly correspond to **small, medium and large deals**:

| Cluster | Avg Qty | Avg Price | Avg Sales | Mostly |
|---|---|---|---|---|
| 0 | 35 | 60 | 2101 | Small deals, cheaper products |
| 1 | 44 | 97 | 5720 | Medium/Large deals, expensive products |
| 2 | 28 | 95 | 3123 | Fewer units of expensive products |

## Concepts
- **Unsupervised learning:** there's no target label. The algorithm finds groups (structure) in the data by itself.
- **Clustering:** grouping similar data points so that points in the same cluster are close together and different clusters are far apart.
- **K-Means algorithm:**
  1. Choose k and initialise k centroids (`k-means++` spreads the initial centroids out smartly).
  2. **Assign** each point to its nearest centroid (Euclidean distance).
  3. **Update** each centroid to the mean of its assigned points.
  4. Repeat steps 2–3 until the centroids stop moving.
  `n_init=10` runs the algorithm 10 times with different starts and keeps the best result.
- **WCSS / inertia:** the Within-Cluster Sum of Squares, i.e. the sum of squared distances from each point to its centroid. Lower means tighter clusters.
- **Elbow method:** plot WCSS against k. WCSS always decreases as k grows. The **elbow** is the point where adding another cluster stops giving a big improvement.
- **Silhouette score** (–1 to 1) is printed as a second check of how well separated the clusters are.
- **Feature selection and scaling:** IDs, dates, names, phone numbers and addresses aren't behaviour, so only QUANTITYORDERED, PRICEEACH, SALES and MSRP are used. They're scaled with `StandardScaler`, because K-Means is distance-based and SALES (thousands) would otherwise dominate.
- **Hierarchical (agglomerative) clustering:** every point starts as its own cluster, and the two closest clusters are merged repeatedly. **Ward linkage** merges the pair that increases total variance the least. The **dendrogram** shows the merge tree, and cutting it at the largest vertical gap gives the number of clusters. Unlike K-Means, you don't need to pick k in advance.

## Code walkthrough
1. Load with `encoding="latin1"` and inspect.
2. Select the four numeric features, `dropna`, then `StandardScaler`.
3. Elbow loop for k = 1–10: store `inertia_`, plot it, and print the WCSS and silhouette scores.
4. Fit `KMeans(n_clusters=3)` and print the cluster sizes, the average features per cluster and a cross-tab against the real `DEALSIZE`. Scatter plot with centroids (converted back to the original scale with `inverse_transform`).
5. `linkage(X, "ward")` and a truncated dendrogram, then `AgglomerativeClustering(n_clusters=3)` and its cluster summary.
