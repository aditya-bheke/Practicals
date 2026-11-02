# Practical 10 – K-Nearest Neighbors on the Diabetes Dataset

**Aim:** Implement the K-Nearest Neighbors algorithm on `diabetes.csv`. Compute the confusion matrix, accuracy, error rate, precision and recall.

## Files
| File | Purpose |
|---|---|
| `knn_diabetes.py` | Plain Python script |
| `knn_diabetes.ipynb` | Same code as a Jupyter notebook |
| `diabetes.csv` | Pima Indians Diabetes dataset: 768 patients, 8 features + `Outcome` (Kaggle) |

## Setup and run
Do the one-time setup in the main `README.md` first. Then:
```bash
cd Practical_10_KNN_Diabetes
python knn_diabetes.py
# or
jupyter notebook knn_diabetes.ipynb
```
It runs in a few seconds.

## Input guide
This program needs **no keyboard input**. It reads the CSV file in this folder automatically. Just run it from inside this folder.
When run as a `.py` script, each graph opens in its own window, and the program **continues only after you close that window**.

## Results obtained
Best k = 19 (chosen by 5-fold cross-validation)
```
Confusion matrix:      Predicted 0  Predicted 1
         Actual 0          85           15
         Actual 1          24           30
Accuracy   : 0.7468
Error rate : 0.2532
Precision  : 0.6667
Recall     : 0.5556
```

## Concepts
- **KNN:** a supervised, **non-parametric**, **lazy** algorithm. To classify a patient, it finds the **k nearest** training patients by **Euclidean distance** `√Σ(xi − yi)²` and takes the majority class.
- **Choosing k:** a small k (like 1) overfits and is noisy. A large k underfits. **Odd k** avoids ties. Here k is chosen with **k-fold cross-validation**: the training data is split into 5 parts, and each part takes a turn as the validation set. The k with the lowest average error is kept, and the error-rate-vs-k plot shows this.
- **Handling invalid zeros:** Glucose, BloodPressure, SkinThickness, Insulin and BMI can't really be 0. In this dataset 0 means missing, so those zeros are replaced with the column **median**, which is robust to outliers.
- **Feature scaling:** KNN is distance-based, so features must be on the same scale. Otherwise Insulin (0–846) would dominate Pedigree (0–2.4). `StandardScaler` is used.
- **Confusion matrix and metrics:**

|             | Predicted 0 | Predicted 1 |
|-------------|-------------|-------------|
| **Actual 0** | TN | FP |
| **Actual 1** | FN | TP |

  - **Accuracy** = (TP+TN)/Total: overall correctness
  - **Error rate** = (FP+FN)/Total = 1 − Accuracy
  - **Precision** = TP/(TP+FP): of the patients predicted diabetic, how many actually are
  - **Recall (sensitivity)** = TP/(TP+FN): of the actual diabetics, how many were detected. In medical diagnosis, recall is critical because missing a sick patient is costly.

## Code walkthrough
1. Load the CSV and show `describe()` and the outcome counts.
2. Replace invalid zeros with the median, then draw a correlation heatmap. Glucose has the strongest correlation with the outcome.
3. Stratified 80/20 split and `StandardScaler`.
4. Loop over k = 1, 3, …, 25 with `cross_val_score(cv=5)`, plot the error rate and pick the best k.
5. Train the final `KNeighborsClassifier(best_k)` and predict.
6. Unpack `confusion_matrix(...).ravel()` into TN, FP, FN, TP. Compute each metric **by formula**, then cross-check with sklearn's `accuracy_score`, `precision_score` and `recall_score`, and draw a heatmap.
