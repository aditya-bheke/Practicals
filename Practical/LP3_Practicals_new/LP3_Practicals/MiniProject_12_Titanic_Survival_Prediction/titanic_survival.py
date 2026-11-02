# %% [markdown]
# # Mini Project (Group B) : Titanic Survival Prediction
# Build a machine learning model that predicts which passengers survived the Titanic shipwreck
# using passenger data (name, age, gender, socio-economic class, etc.).
#
# Dataset (Kaggle "Titanic - Machine Learning from Disaster"), kept in this folder:
# * `train.csv` - 891 passengers **with** the `Survived` label (0 = died, 1 = survived) -> used to train and evaluate
# * `test.csv`  - 418 passengers **without** the label -> we predict them and write `submission.csv`
#
# Steps: explore -> clean -> feature engineering -> train several classifiers -> compare -> tune -> predict.

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# %% [markdown]
# ## 1. Load the data

# %%
train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")
print("Train shape:", train.shape, " Test shape:", test.shape)
print(train.head())
print("\nMissing values in train:\n", train.isnull().sum())

# %% [markdown]
# ## 2. Exploratory Data Analysis (EDA)
# Who survived? Women and children first, and first-class passengers had better access to lifeboats.

# %%
print("Overall survival rate:", round(train["Survived"].mean(), 3))
print("\nSurvival rate by Sex:\n", train.groupby("Sex")["Survived"].mean().round(3))
print("\nSurvival rate by Pclass:\n", train.groupby("Pclass")["Survived"].mean().round(3))

fig, axes = plt.subplots(1, 3, figsize=(16, 4))
sns.countplot(x="Survived", hue="Sex", data=train, ax=axes[0])
axes[0].set_title("Survival by Sex")
sns.countplot(x="Pclass", hue="Survived", data=train, ax=axes[1])
axes[1].set_title("Survival by Passenger Class")
sns.histplot(data=train, x="Age", hue="Survived", bins=30, kde=True, ax=axes[2])
axes[2].set_title("Age distribution by Survival")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 3. Data cleaning and feature engineering
# Applied identically to train and test (combined first so both get the same columns).
# * **Title** extracted from Name (Mr, Mrs, Miss, Master, Rare), which carries gender, age and status
# * **Age** missing (~20%) -> filled with the median age of passengers having the same Title
# * **Embarked** missing (2 rows) -> most frequent port; **Fare** missing (1 test row) -> median
# * **FamilySize** = SibSp + Parch + 1, and **IsAlone**
# * **HasCabin** (Cabin is 77% missing, but *having* a cabin number correlates with class)
# * Text columns -> numbers: Sex mapped to 0/1; Embarked and Title one-hot encoded
# * Dropped: PassengerId, Name, Ticket, Cabin (identifiers / free text)

# %%
full = pd.concat([train.drop(columns=["Survived"]), test], ignore_index=True)

full["Title"] = full["Name"].str.extract(r",\s*([^\.]+)\.", expand=False).str.strip()
full["Title"] = full["Title"].replace({"Mlle": "Miss", "Ms": "Miss", "Mme": "Mrs"})
full.loc[~full["Title"].isin(["Mr", "Mrs", "Miss", "Master"]), "Title"] = "Rare"

full["Age"] = full["Age"].fillna(full.groupby("Title")["Age"].transform("median"))
full["Embarked"] = full["Embarked"].fillna(full["Embarked"].mode()[0])
full["Fare"] = full["Fare"].fillna(full["Fare"].median())

full["FamilySize"] = full["SibSp"] + full["Parch"] + 1
full["IsAlone"] = (full["FamilySize"] == 1).astype(int)
full["HasCabin"] = full["Cabin"].notnull().astype(int)
full["Sex"] = full["Sex"].map({"male": 0, "female": 1})

full = full.drop(columns=["PassengerId", "Name", "Ticket", "Cabin"])
full = pd.get_dummies(full, columns=["Embarked", "Title"], drop_first=True, dtype=int)

X_all = full.iloc[:len(train)]
X_kaggle_test = full.iloc[len(train):]
y_all = train["Survived"]
print("Features used:", list(X_all.columns))
print("Missing values left:", X_all.isnull().sum().sum())

plt.figure(figsize=(12, 8))
sns.heatmap(pd.concat([X_all, y_all], axis=1).corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation matrix")
plt.show()

# %% [markdown]
# ## 4. Train / validation split
# `test.csv` has no labels, so we hold out 20% of `train.csv` to measure accuracy.

# %%
X_train, X_val, y_train, y_val = train_test_split(X_all, y_all, test_size=0.2,
                                                  random_state=42, stratify=y_all)
print("Train:", X_train.shape, " Validation:", X_val.shape)

# %% [markdown]
# ## 5. Train and compare several classifiers
# Models that need scaled inputs (Logistic Regression, KNN, SVM) are wrapped in a pipeline with
# StandardScaler. Each is scored by **validation accuracy** and **5-fold cross-validation**.

# %%
models = {
    "Logistic Regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "KNN (k=7)": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=7)),
    "SVM (RBF)": make_pipeline(StandardScaler(), SVC(kernel="rbf")),
    "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=7, random_state=42),
}

results = []
for name, model in models.items():
    model.fit(X_train, y_train)
    val_acc = accuracy_score(y_val, model.predict(X_val))
    cv_acc = cross_val_score(model, X_all, y_all, cv=5).mean()
    results.append({"Model": name, "Validation accuracy": val_acc, "5-fold CV accuracy": cv_acc})

results = pd.DataFrame(results).sort_values("5-fold CV accuracy", ascending=False)
print(results.round(4).to_string(index=False))

results.set_index("Model")[["Validation accuracy", "5-fold CV accuracy"]].plot(
    kind="bar", figsize=(9, 4), ylim=(0.6, 0.9))
plt.title("Model comparison")
plt.xticks(rotation=20)
plt.show()

# %% [markdown]
# ## 6. Tune the Random Forest (GridSearchCV)
# Try combinations of hyper-parameters with 5-fold cross-validation and keep the best.

# %%
param_grid = {"n_estimators": [100, 300], "max_depth": [4, 6, 8], "min_samples_split": [2, 5]}
grid = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, n_jobs=-1)
grid.fit(X_train, y_train)
best_rf = grid.best_estimator_
print("Best parameters:", grid.best_params_)
print("Best CV accuracy:", round(grid.best_score_, 4))

y_pred = best_rf.predict(X_val)
print("\nTuned Random Forest - validation accuracy:", round(accuracy_score(y_val, y_pred), 4))
print("\nConfusion matrix:\n", confusion_matrix(y_val, y_pred))
print("\n", classification_report(y_val, y_pred, target_names=["Died", "Survived"]))

sns.heatmap(confusion_matrix(y_val, y_pred), annot=True, fmt="d", cmap="Blues",
            xticklabels=["Died", "Survived"], yticklabels=["Died", "Survived"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Tuned Random Forest - confusion matrix")
plt.show()

importances = pd.Series(best_rf.feature_importances_, index=X_all.columns).sort_values()
importances.plot(kind="barh", figsize=(8, 5), title="Which features matter most?")
plt.show()

# %% [markdown]
# ## 7. Predict the unlabeled test.csv and save submission.csv
# Retrain the tuned model on **all** 891 labelled passengers, then predict the 418 test passengers.
# `submission.csv` (PassengerId, Survived) is in the format Kaggle accepts.

# %%
final_model = RandomForestClassifier(random_state=42, **grid.best_params_)
final_model.fit(X_all, y_all)
test_pred = final_model.predict(X_kaggle_test)

submission = pd.DataFrame({"PassengerId": test["PassengerId"], "Survived": test_pred})
submission.to_csv("submission.csv", index=False)
print("Saved submission.csv with", len(submission), "predictions")
print("Predicted survival rate on test set:", round(test_pred.mean(), 3))
print(submission.head())

# %% [markdown]
# ## 8. Predict for a new passenger (demo)
# Change the values below to try your own passenger.


# %%
def predict_passenger(pclass, sex, age, sibsp, parch, fare, embarked, title):
    row = {"Pclass": pclass, "Sex": 1 if sex == "female" else 0, "Age": age, "SibSp": sibsp,
           "Parch": parch, "Fare": fare, "FamilySize": sibsp + parch + 1,
           "IsAlone": int(sibsp + parch == 0), "HasCabin": int(pclass == 1)}
    for col in X_all.columns:
        if col.startswith("Embarked_"):
            row[col] = int(col == f"Embarked_{embarked}")
        elif col.startswith("Title_"):
            row[col] = int(col == f"Title_{title}")
    X_new = pd.DataFrame([row])[X_all.columns]
    prob = final_model.predict_proba(X_new)[0][1]
    return prob


examples = [
    ("1st-class woman, 30, travelling alone", (1, "female", 30, 0, 0, 80.0, "C", "Mrs")),
    ("3rd-class man, 25, travelling alone", (3, "male", 25, 0, 0, 7.9, "S", "Mr")),
    ("2nd-class boy, 6, with parents", (2, "male", 6, 0, 2, 26.0, "S", "Master")),
]
for label, args in examples:
    print(f"{label:<40} -> survival probability {predict_passenger(*args):.2f}")
