# Mini Project (Group B) – Titanic Survival Prediction

**Problem statement (SPPU syllabus):** Build a machine learning model that predicts the type of people who survived the Titanic shipwreck using passenger data (i.e. name, age, gender, socio-economic class, etc.).

## Files
| File | Purpose |
|---|---|
| `titanic_survival.py` | Plain Python script |
| `titanic_survival.ipynb` | Same code as a Jupyter notebook, with explanations |
| `train.csv` | 891 passengers **with** the `Survived` label ([Kaggle source](https://www.kaggle.com/competitions/titanic/data)) |
| `test.csv` | 418 passengers **without** the label (Kaggle's test set) |
| `submission.csv` | *Created when you run the code*: predictions for test.csv in Kaggle's format |

## Setup and run
Do the one-time setup in the main `README.md` first (Python + `pip install -r requirements.txt`). Then:
```bash
cd MiniProject_12_Titanic_Survival_Prediction
python titanic_survival.py
# or
jupyter notebook titanic_survival.ipynb     # then Kernel > Restart & Run All
```
It takes about 15–30 seconds, mostly for the GridSearch.

## Input guide
**No keyboard input is needed.** The program reads `train.csv` and `test.csv` from this folder. Close each graph window to continue when running the `.py` script.
To try **your own passenger**, edit the `examples` list in the last section (class, sex, age, siblings/spouses, parents/children, fare, port C/Q/S, title Mr/Mrs/Miss/Master/Rare). The program prints that passenger's survival probability.

## Results obtained
| Model | Validation accuracy | 5-fold CV accuracy |
|---|---|---|
| **SVM (RBF)** | 0.827 | **0.831** |
| Logistic Regression | 0.844 | 0.827 |
| Random Forest | 0.821 | 0.822 |
| Decision Tree | 0.782 | 0.805 |
| KNN (k=7) | 0.788 | 0.805 |

- **Tuned Random Forest** (GridSearchCV): best CV accuracy 0.830 with `max_depth=4, n_estimators=300`. Its accuracy on the 179-passenger validation split is 0.80. That number swings a few percent on so few rows, which is why **cross-validation** is the score to trust.
- **Survival rates in the data:** women 74% vs men 19%; 1st class 63%, 2nd 47%, 3rd 24%. This confirms "women and children first" and the class divide.
- **Demo predictions:** 1st-class woman → 0.91, 3rd-class man → 0.12, 2nd-class boy aged 6 → 0.59.
- About 80–83% is the typical honest accuracy for this dataset. Kaggle's top leaderboard scores of 100% come from looking up the real passenger lists.

## Concepts
- **Binary classification:** predict Survived = 1 or 0.
- **EDA (Exploratory Data Analysis):** survival rates by Sex and Pclass, age histograms and correlation heatmaps, to find which features matter *before* modelling.
- **Missing values:** Age is about 20% missing, so it's filled with the **median age of the same title** (a "Master" is a boy, so his median is about 4, not 28). Embarked (2 rows) gets the **mode**, and Fare (1 test row) the **median**. Cabin is 77% missing, so it's replaced by a **HasCabin** flag.
- **Feature engineering**, creating new informative features:
  - **Title** from Name (Mr / Mrs / Miss / Master / Rare), which captures sex, age group and social status at once. It's one of the strongest features.
  - **FamilySize** = SibSp + Parch + 1 and **IsAlone**. People alone, and very large families, had lower survival.
  - **HasCabin**, a proxy for wealth and class.
- **Encoding:** Sex is mapped to 0/1 (binary). Embarked and Title are **one-hot encoded** with `drop_first=True` to avoid the dummy-variable trap.
- **Train and test processed together** (`pd.concat`) so both get exactly the same columns. The labels are never used for this, so there's no leakage.
- **Pipeline (`make_pipeline`):** StandardScaler + model in one object, so scaling is learnt only from the training fold inside cross-validation.
- **Models compared:**
  - **Logistic Regression:** a linear model that outputs a probability through the sigmoid
  - **KNN:** majority vote of the nearest passengers (needs scaling)
  - **SVM (RBF kernel):** a maximum-margin, non-linear boundary
  - **Decision Tree:** if–then splits; `max_depth=5` limits overfitting
  - **Random Forest:** bagging of many decorrelated trees; robust, and gives feature importance
- **Cross-validation (5-fold):** every passenger is used for validation once. It's more reliable than one 80/20 split on a small dataset.
- **Hyperparameter tuning (GridSearchCV):** tries every combination in `param_grid` with cross-validation and keeps the best.
- **Metrics:** accuracy, the confusion matrix, and precision/recall/F1 per class. The model is better at recognising deaths (recall 0.87) than survivals (0.68), because there are fewer survivors (38%).
- **Feature importance** (tuned Random Forest): Sex (0.23) and Title_Mr (0.23) dominate, followed by Fare, HasCabin and Pclass (about 0.08 each). Gender and class mattered most, which matches the history.

## Code walkthrough
1. **Load** both CSVs and show the missing values.
2. **EDA:** survival rates by sex and class, plus three plots.
3. **Clean and engineer:** concat → Title → fill Age/Embarked/Fare → FamilySize, IsAlone, HasCabin → encode → drop ID/text columns → split back into the labelled and unlabelled parts.
4. **Stratified 80/20 split** of the labelled data.
5. **Five classifiers** trained, with validation and 5-fold CV accuracy in a comparison table and bar chart.
6. **GridSearchCV** on Random Forest, then the confusion matrix, classification report and feature-importance chart.
7. **Retrain on all 891 passengers**, predict the 418 in test.csv and save `submission.csv`.
8. `predict_passenger()` builds one feature row with the same columns and prints the survival probability for example passengers.

## Viva points
- Why not drop all rows with a missing Age? You'd lose about 20% of the data. Imputing by title keeps it, with sensible values.
- Why is Title so useful? It combines sex, age and status in one feature: "Master" means a young boy, and young boys were saved first.
- Why not use test.csv for accuracy? It has no Survived column; Kaggle keeps those answers. That's why part of train.csv is held out.
- Why can a tuned model score lower on the validation split? Tuning optimises the CV average. A single split of 179 rows is noisy, so CV is the fairer measure.
- How could you improve it? Gradient boosting (XGBoost), ticket-group features, a fare per person, or ensembling (voting) the top models.
