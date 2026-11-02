# Practical 8 – Email Spam Detection (KNN and SVM)

**Aim:** Classify emails using binary classification: Normal (Not Spam = 0) vs Abnormal (Spam = 1). Use K-Nearest Neighbors and Support Vector Machine, and analyse their performance.

## Files
| File | Purpose |
|---|---|
| `email_spam_detection.py` | Plain Python script |
| `email_spam_detection.ipynb` | Same code as a Jupyter notebook |
| `emails.csv` | Dataset: 5172 emails × 3002 columns ([Kaggle source](https://www.kaggle.com/datasets/balaka18/email-spam-classification-dataset-csv)) |

## Setup and run
Do the one-time setup in the main `README.md` first. Then:
```bash
cd Practical_08_Email_Spam_KNN_SVM
python email_spam_detection.py
# or
jupyter notebook email_spam_detection.ipynb
```
It takes about 15–30 seconds.

## Input guide
This program needs **no keyboard input**. It reads the CSV file in this folder automatically. Just run it from inside this folder.
When run as a `.py` script, each graph opens in its own window, and the program **continues only after you close that window**.

## Results obtained
| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| KNN (k=5) | 0.872 | 0.746 | 0.843 | 0.792 |
| **SVM (linear)** | **0.972** | **0.939** | **0.967** | **0.952** |

**Analysis:** SVM clearly outperforms KNN. With 3000 features, distances between points become less meaningful (the **curse of dimensionality**), which hurts KNN. A linear SVM handles high-dimensional text data very well.

## Concepts
- **Binary classification:** the output is one of two classes (spam / not spam).
- **Dataset format (bag of words):** each column is one of the 3000 most common words, and each cell is how many times that word appears in that email.
- **KNN (K-Nearest Neighbors):** a **lazy learner**, meaning there's no training phase and it just stores the data. For a new email it finds the k closest emails (Euclidean distance) and takes the **majority vote**. Small k makes the model sensitive to noise. Large k makes it over-smoothed. The code tries k = 1, 3, …, 15 and plots the accuracy.
- **SVM (Support Vector Machine):** finds the **hyperplane** that separates the two classes with the **maximum margin**. The points closest to the hyperplane are the **support vectors**. `C` controls the trade-off between a wide margin and misclassifying training points (small C means a wider, more regularised margin). **Kernels** (linear, RBF, polynomial) allow non-linear boundaries. Linear works best for text.
- **Feature scaling (StandardScaler)** is used for SVM. For KNN on raw word counts, the unscaled data gave better accuracy in this dataset.
- **Stratified split** keeps the same spam/not-spam ratio (about 29% spam) in the train and test sets.
- **Evaluation:** the **confusion matrix** (TP, TN, FP, FN), plus accuracy, precision (`TP/(TP+FP)`), recall (`TP/(TP+FN)`) and F1. For spam filtering, a **false positive** (a real email sent to spam) is costly, so precision matters.

## Code walkthrough
1. Load the CSV, check for missing values, and plot the class distribution.
2. Drop `Email No.`, then X = word counts and y = `Prediction`. Do a stratified 80/20 split and scale for SVM.
3. KNN: loop over k, plot accuracy and keep the best k, then train the final model.
4. SVM: `SVC(kernel="linear", C=0.01)` on scaled data.
5. `report()` prints a classification report for each model and builds a comparison table. Then confusion-matrix heatmaps and a comparison bar chart are plotted.
