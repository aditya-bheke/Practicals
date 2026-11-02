# %% [markdown]
# # Practical 7 : Uber Ride Fare Prediction
# **Tasks**
# 1. Pre-process the dataset
# 2. Identify outliers
# 3. Check the correlation
# 4. Implement Linear Regression and Random Forest Regression models
# 5. Evaluate the models and compare their R2, RMSE, etc.
#
# Dataset: `uber.csv` (Kaggle - yasserh/uber-fares-dataset), kept in this folder.

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# %% [markdown]
# ## 1. Load the dataset

# %%
df = pd.read_csv("uber.csv")
print("Shape:", df.shape)
print(df.head())
df.info()

# %% [markdown]
# ## 2. Pre-processing
# * Drop the useless columns (`Unnamed: 0` index column and `key`)
# * Remove rows with missing values
# * Convert `pickup_datetime` to a datetime and extract hour, day, month, year, weekday
# * Compute the trip **distance** (in km) from the pickup/drop-off coordinates using the Haversine formula

# %%
df = df.drop(columns=["Unnamed: 0", "key"], errors="ignore")
print("Missing values before:\n", df.isnull().sum())
df = df.dropna()

df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], errors="coerce")
df = df.dropna(subset=["pickup_datetime"])
df["hour"] = df["pickup_datetime"].dt.hour
df["day"] = df["pickup_datetime"].dt.day
df["month"] = df["pickup_datetime"].dt.month
df["year"] = df["pickup_datetime"].dt.year
df["dayofweek"] = df["pickup_datetime"].dt.dayofweek
df = df.drop(columns=["pickup_datetime"])


def haversine(lon1, lat1, lon2, lat2):
    """Great-circle distance between two points on Earth, in km."""
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 6371 * 2 * np.arcsin(np.sqrt(a))


df["distance_km"] = haversine(df["pickup_longitude"], df["pickup_latitude"],
                              df["dropoff_longitude"], df["dropoff_latitude"])
print(df.describe().T)

# %% [markdown]
# ## 3. Identify outliers
# Box plots show the outliers visually. They are then removed:
# * invalid values: coordinates outside valid latitude/longitude, fare <= 0, passengers 0 or > 6, distance 0
# * statistical outliers in fare and distance using the **IQR rule** (outside Q1 - 1.5*IQR, Q3 + 1.5*IQR)

# %%
cols = ["fare_amount", "distance_km", "passenger_count"]
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, c in zip(axes, cols):
    sns.boxplot(x=df[c], ax=ax)
    ax.set_title(f"{c} (before)")
plt.tight_layout()
plt.show()

print("Rows before outlier removal:", len(df))
df = df[(df["pickup_latitude"].between(-90, 90)) & (df["dropoff_latitude"].between(-90, 90)) &
        (df["pickup_longitude"].between(-180, 180)) & (df["dropoff_longitude"].between(-180, 180))]
df = df[(df["fare_amount"] > 0) & (df["passenger_count"].between(1, 6)) & (df["distance_km"] > 0)]


def remove_outliers_iqr(data, column):
    q1, q3 = data[column].quantile([0.25, 0.75])
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return data[(data[column] >= low) & (data[column] <= high)]


for c in ["fare_amount", "distance_km"]:
    df = remove_outliers_iqr(df, c)
print("Rows after outlier removal :", len(df))

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, c in zip(axes, cols):
    sns.boxplot(x=df[c], ax=ax)
    ax.set_title(f"{c} (after)")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 4. Check the correlation
# Values close to +1 or -1 mean a strong linear relationship. `distance_km` should be the
# feature most correlated with `fare_amount`.

# %%
corr = df.corr()
plt.figure(figsize=(11, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation matrix")
plt.show()
print("Correlation with fare_amount:\n", corr["fare_amount"].sort_values(ascending=False))

# %% [markdown]
# ## 5. Train-test split and scaling

# %%
X = df.drop(columns=["fare_amount"])
y = df["fare_amount"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)
print("Train:", X_train.shape, " Test:", X_test.shape)

# %% [markdown]
# ## 6. Linear Regression

# %%
lr = LinearRegression()
lr.fit(X_train_s, y_train)
y_pred_lr = lr.predict(X_test_s)

# %% [markdown]
# ## 7. Random Forest Regression
# (100 trees; `n_jobs=-1` uses all CPU cores. It can take a minute or two.)

# %%
rf = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

# %% [markdown]
# ## 8. Evaluate and compare
# * **R2** - share of the fare's variance explained by the model (1 = perfect)
# * **RMSE** - root mean squared error, in dollars (lower is better)
# * **MAE** - mean absolute error, in dollars


# %%
def evaluate(name, y_true, y_pred):
    return {"Model": name,
            "R2": r2_score(y_true, y_pred),
            "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
            "MAE": mean_absolute_error(y_true, y_pred)}


results = pd.DataFrame([evaluate("Linear Regression", y_test, y_pred_lr),
                        evaluate("Random Forest", y_test, y_pred_rf)])
print(results.to_string(index=False))

importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values()
importances.plot(kind="barh", figsize=(8, 5), title="Random Forest feature importance")
plt.show()

plt.figure(figsize=(6, 6))
plt.scatter(y_test[:2000], y_pred_rf[:2000], s=5, alpha=0.5)
plt.plot([0, y_test.max()], [0, y_test.max()], "r--")
plt.xlabel("Actual fare")
plt.ylabel("Predicted fare (Random Forest)")
plt.title("Actual vs Predicted")
plt.show()
