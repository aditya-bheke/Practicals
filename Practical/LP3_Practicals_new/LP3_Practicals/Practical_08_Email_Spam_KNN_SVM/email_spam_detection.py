# %% [markdown]
# # Practical 8 : Email Spam Detection using KNN and SVM
# Classify emails using binary classification:
# * **0 - Normal (Not Spam)**
# * **1 - Abnormal (Spam)**
#
# Use **K-Nearest Neighbors** and **Support Vector Machine** and analyse their performance.
#
# Dataset: `emails.csv` (Kaggle - balaka18/email-spam-classification-dataset-csv), kept in this folder.
# 5172 rows (emails) x 3002 columns: `Email No.`, 3000 word-count columns, `Prediction` (label).

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report)

# %% [markdown]
# ## 1. Load and inspect the dataset

# %%
df = pd.read_csv("emails.csv")
print("Shape:", df.shape)
print(df.iloc[:5, :10])
print("Missing values:", df.isnull().sum().sum())
print("\nClass distribution (0 = Not Spam, 1 = Spam):")
print(df["Prediction"].value_counts())

sns.countplot(x="Prediction", data=df)
plt.title("Not Spam (0) vs Spam (1)")
plt.show()

# %% [markdown]
# ## 2. Pre-processing
# * Drop `Email No.` (just an identifier, not a feature)
# * X = 3000 word counts, y = `Prediction`
# * Split 80/20 with `stratify=y` so both sets keep the same spam ratio
# * Scale the features. KNN uses distances and SVM uses margins, so features on a common scale matter.

# %%
X = df.drop(columns=["Email No.", "Prediction"])
y = df["Prediction"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=42, stratify=y)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)
print("Train:", X_train.shape, " Test:", X_test.shape)

# %% [markdown]
# ## 3. K-Nearest Neighbors
# A new email gets the majority class of its *k* closest emails (Euclidean distance).
# First try several values of k and keep the best one.

# %%
k_values = range(1, 16, 2)
knn_acc = []
for k in k_values:
    m = KNeighborsClassifier(n_neighbors=k)
    m.fit(X_train, y_train)
    knn_acc.append(accuracy_score(y_test, m.predict(X_test)))
best_k = list(k_values)[int(np.argmax(knn_acc))]

plt.plot(list(k_values), knn_acc, marker="o")
plt.xlabel("k (number of neighbours)")
plt.ylabel("Accuracy")
plt.title("KNN accuracy for different k")
plt.show()
print("Best k =", best_k)

knn = KNeighborsClassifier(n_neighbors=best_k)
knn.fit(X_train, y_train)          # raw word counts work better than scaled ones for KNN here
y_pred_knn = knn.predict(X_test)

# %% [markdown]
# ## 4. Support Vector Machine
# SVM finds the hyperplane that separates the two classes with the **maximum margin**.
# A linear kernel suits high-dimensional text data well.

# %%
svm = SVC(kernel="linear", C=0.01)
svm.fit(X_train_s, y_train)
y_pred_svm = svm.predict(X_test_s)

# %% [markdown]
# ## 5. Analyse the performance
# * **Accuracy** = correct / total
# * **Precision** = TP / (TP + FP): of the emails flagged as spam, how many really are spam
# * **Recall** = TP / (TP + FN): of all real spam, how much was caught
# * **F1** = harmonic mean of precision and recall


# %%
def report(name, y_pred):
    print(f"\n===== {name} =====")
    print("Accuracy :", round(accuracy_score(y_test, y_pred), 4))
    print(classification_report(y_test, y_pred, target_names=["Not Spam", "Spam"]))
    return {"Model": name,
            "Accuracy": accuracy_score(y_test, y_pred),
            "Precision": precision_score(y_test, y_pred),
            "Recall": recall_score(y_test, y_pred),
            "F1": f1_score(y_test, y_pred)}


results = pd.DataFrame([report(f"KNN (k={best_k})", y_pred_knn),
                        report("SVM (linear)", y_pred_svm)])
print(results.round(4).to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
for ax, (name, pred) in zip(axes, [("KNN", y_pred_knn), ("SVM", y_pred_svm)]):
    sns.heatmap(confusion_matrix(y_test, pred), annot=True, fmt="d", cmap="Blues",
                xticklabels=["Not Spam", "Spam"], yticklabels=["Not Spam", "Spam"], ax=ax)
    ax.set_title(f"{name} confusion matrix")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
plt.tight_layout()
plt.show()

results.set_index("Model")[["Accuracy", "Precision", "Recall", "F1"]].plot(kind="bar", figsize=(8, 4), ylim=(0.5, 1))
plt.title("KNN vs SVM")
plt.xticks(rotation=0)
plt.show()
