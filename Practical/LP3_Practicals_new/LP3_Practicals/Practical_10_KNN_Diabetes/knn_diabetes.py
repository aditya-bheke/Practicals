# %% [markdown]
# # Practical 10 : K-Nearest Neighbors on diabetes.csv
# Implement KNN to predict whether a patient has diabetes (`Outcome = 1`) or not (`Outcome = 0`),
# then compute the **confusion matrix, accuracy, error rate, precision and recall**.
#
# Dataset: `diabetes.csv` (Pima Indians Diabetes dataset from Kaggle), kept in this folder.
# Columns: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, Pedigree, Age, Outcome

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (confusion_matrix, accuracy_score, precision_score,
                             recall_score, classification_report)

# %% [markdown]
# ## 1. Load the dataset

# %%
df = pd.read_csv("diabetes.csv")
print("Shape:", df.shape)
print(df.head())
print(df.describe().T)
print("\nOutcome counts:\n", df["Outcome"].value_counts())

# %% [markdown]
# ## 2. Pre-processing: handle invalid zeros
# A value of 0 is impossible for Glucose, BloodPressure, SkinThickness, Insulin and BMI, so in this
# dataset 0 really means "missing". These zeros are replaced with the **median** of the column.

# %%
zero_invalid = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
print("Zero counts before:\n", (df[zero_invalid] == 0).sum())
for col in zero_invalid:
    df[col] = df[col].replace(0, np.nan)
    df[col] = df[col].fillna(df[col].median())
print("\nZero counts after:\n", (df[zero_invalid] == 0).sum())

plt.figure(figsize=(9, 7))
sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation matrix")
plt.show()

# %% [markdown]
# ## 3. Split and scale
# KNN uses **distances**, so every feature must be on the same scale. Otherwise a large-valued
# feature like Insulin would dominate a small one like Pedigree.

# %%
X = df.drop(columns=["Outcome"])
y = df["Outcome"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=42, stratify=y)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# %% [markdown]
# ## 4. Choose k
# Try k = 1..25 and use **5-fold cross-validation** on the training set to pick the best k.
# Odd k avoids ties between the two classes.

# %%
k_range = range(1, 26, 2)
cv_scores = [cross_val_score(KNeighborsClassifier(n_neighbors=k), X_train_s, y_train, cv=5).mean()
             for k in k_range]
best_k = list(k_range)[int(np.argmax(cv_scores))]

plt.plot(list(k_range), [1 - s for s in cv_scores], marker="o")
plt.xlabel("k")
plt.ylabel("Cross-validation error rate")
plt.title("Error rate vs k")
plt.show()
print("Best k =", best_k)

# %% [markdown]
# ## 5. Train the final KNN model and predict

# %%
knn = KNeighborsClassifier(n_neighbors=best_k)
knn.fit(X_train_s, y_train)
y_pred = knn.predict(X_test_s)

# %% [markdown]
# ## 6. Confusion matrix, accuracy, error rate, precision, recall
# |             | Predicted 0 | Predicted 1 |
# |-------------|-------------|-------------|
# | **Actual 0** | TN          | FP          |
# | **Actual 1** | FN          | TP          |
#
# * Accuracy  = (TP + TN) / total
# * Error rate = (FP + FN) / total = 1 - accuracy
# * Precision = TP / (TP + FP)
# * Recall    = TP / (TP + FN)

# %%
cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()
total = tn + fp + fn + tp

accuracy = (tp + tn) / total
error_rate = (fp + fn) / total
precision = tp / (tp + fp)
recall = tp / (tp + fn)

print("Confusion matrix:\n", cm)
print(f"\nTP={tp}  TN={tn}  FP={fp}  FN={fn}")
print(f"Accuracy   : {accuracy:.4f}")
print(f"Error rate : {error_rate:.4f}")
print(f"Precision  : {precision:.4f}")
print(f"Recall     : {recall:.4f}")

# Cross-check with scikit-learn's built-in functions
print("\n(sklearn) accuracy =", round(accuracy_score(y_test, y_pred), 4),
      " precision =", round(precision_score(y_test, y_pred), 4),
      " recall =", round(recall_score(y_test, y_pred), 4))
print("\n", classification_report(y_test, y_pred, target_names=["No diabetes", "Diabetes"]))

sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["No diabetes", "Diabetes"], yticklabels=["No diabetes", "Diabetes"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title(f"KNN (k={best_k}) confusion matrix")
plt.show()
