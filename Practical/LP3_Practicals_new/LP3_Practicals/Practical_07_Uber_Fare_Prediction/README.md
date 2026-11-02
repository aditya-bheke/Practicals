# Practical 7 – Uber Ride Fare Prediction

**Aim:** Predict the price of an Uber ride from a pickup point to the drop-off location.
1. Pre-process the dataset 2. Identify outliers 3. Check the correlation 4. Implement Linear Regression and Random Forest Regression 5. Evaluate and compare the models using R2, RMSE, etc.

## Files
| File | Purpose |
|---|---|
| `uber_fare_prediction.py` | Plain Python script |
| `uber_fare_prediction.ipynb` | Same code as a Jupyter notebook, with explanations between cells |
| `uber.csv` | Dataset: 200,000 rides ([Kaggle source](https://www.kaggle.com/datasets/yasserh/uber-fares-dataset)) |

## Setup and run
Do the one-time setup in the main `README.md` first (install Python and `pip install -r requirements.txt`). Then:
```bash
cd Practical_07_Uber_Fare_Prediction
python uber_fare_prediction.py        # graphs open in windows; close each one to continue
# or
jupyter notebook uber_fare_prediction.ipynb   # then Kernel > Restart & Run All
```
Always run from **inside this folder**, so that `uber.csv` is found. The whole script takes about 30–60 seconds, mostly for the Random Forest.

## Input guide
This program needs **no keyboard input**. It reads the CSV file in this folder automatically. Just run it from inside this folder.
When run as a `.py` script, each graph opens in its own window, and the program **continues only after you close that window**.

## Results obtained (your numbers may vary slightly)
| Model | R2 | RMSE ($) | MAE ($) |
|---|---|---|---|
| Linear Regression | 0.673 | 2.13 | 1.52 |
| **Random Forest** | **0.742** | **1.89** | **1.31** |

Random Forest wins because the fare doesn't depend on the features in a purely straight-line way.

## Concepts
- **Regression:** predicting a continuous number (the fare), as opposed to a class.
- **Pre-processing:** removing useless columns (`Unnamed: 0`, `key`), dropping missing values, and **feature engineering**. Hour, day, month, year and weekday are extracted from `pickup_datetime`, and **distance** is calculated from latitude/longitude using the **Haversine formula** (great-circle distance on a sphere of radius 6371 km).
- **Outliers:** values far from the rest, such as a fare of –$50, 208 passengers, or a 16,000 km trip. **Box plots** show them visually. They're removed with validity rules and the **IQR rule**: keep values in `[Q1 − 1.5·IQR, Q3 + 1.5·IQR]`, where `IQR = Q3 − Q1`.
- **Correlation:** Pearson coefficient from –1 to +1, shown as a **heatmap**. `distance_km` has about 0.80 correlation with the fare, so it's the strongest predictor.
- **Linear Regression:** fits `fare = b0 + b1·x1 + … + bn·xn` by minimising squared error.
- **Random Forest Regression:** an **ensemble** of many decision trees, each trained on a random sample of rows and features (**bagging**). The prediction is the average of all trees. It handles non-linear patterns and is robust to noise.
- **Metrics:**
  - **R2** = 1 − SS_res/SS_tot. It's the fraction of the fare's variance explained (1 = perfect).
  - **RMSE** = √(mean of squared errors). It's in dollars and penalises big errors more.
  - **MAE** = mean of the absolute errors, also in dollars.
- **Train-test split** (80/20) checks performance on unseen data. **StandardScaler** puts features on the same scale for Linear Regression. Random Forest doesn't need scaling.

## Code walkthrough
1. **Load:** `pd.read_csv`, `df.info()`.
2. **Pre-process:** drop columns, `dropna`, convert the datetime and extract its parts, apply `haversine()` to get `distance_km`.
3. **Outliers:** box plots before, then remove invalid coordinates, fares ≤ 0, passengers outside 1–6 and zero distances, then apply `remove_outliers_iqr()` to fare and distance. Box plots after.
4. **Correlation:** `df.corr()` plus a seaborn heatmap, with features sorted by correlation with the fare.
5. **Split and scale:** `train_test_split`, `StandardScaler`.
6. **Models:** `LinearRegression()` and `RandomForestRegressor(n_estimators=100, max_depth=15)`.
7. **Evaluate:** an `evaluate()` helper builds the comparison table. There's also a feature-importance bar chart and an actual-vs-predicted scatter plot.
