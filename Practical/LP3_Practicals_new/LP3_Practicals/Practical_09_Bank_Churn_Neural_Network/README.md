# Practical 9 – Bank Customer Churn Prediction (Neural Network)

**Aim:** Given a bank customer, build a neural-network classifier that determines whether they will leave the bank in the next 6 months.
1. Read the dataset 2. Separate the features and target, and split into train/test 3. Normalize 4. Build the model, identify points of improvement and implement them 5. Print the accuracy and confusion matrix

## Files
| File | Purpose |
|---|---|
| `bank_churn_ann.py` | Plain Python script |
| `bank_churn_ann.ipynb` | Same code as a Jupyter notebook |
| `Churn_Modelling.csv` | Dataset: 10,000 customers, 14 columns ([Kaggle source](https://www.kaggle.com/barelydedicated/bank-customer-churn-modeling)) |

## Setup and run
This practical needs **TensorFlow** in addition to the common libraries. `requirements.txt` already includes it.
- TensorFlow supports **64-bit Python 3.9–3.12** (newer versions also support 3.13). If `pip install tensorflow` says *"No matching distribution found"*, your Python is too new or 32-bit. Install Python 3.11 or 3.12 (64-bit) and recreate the virtual environment.
- Windows: if `import tensorflow` gives a DLL error, install the [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist) and restart.
- Macs with Apple Silicon (M1/M2/M3): `pip install tensorflow` works directly.

```bash
cd Practical_09_Bank_Churn_Neural_Network
python bank_churn_ann.py
# or
jupyter notebook bank_churn_ann.ipynb
```
Training prints a progress line per epoch and takes about 1–2 minutes on a normal laptop. No GPU is needed.

**Expected result:** about **85–87% accuracy** for the improved model, slightly better than the basic model. Neural-network results vary a little between machines and TensorFlow versions, even with a fixed seed.

## Input guide
This program needs **no keyboard input**. It reads the CSV file in this folder automatically. Just run it from inside this folder.
When run as a `.py` script, each graph opens in its own window, and the program **continues only after you close that window**.

## Concepts
- **Customer churn:** a customer leaving a service. The target column is `Exited` (1 = left). About 20% of customers churned, so the classes are **imbalanced**.
- **Feature/target separation:** `RowNumber`, `CustomerId` and `Surname` are identifiers with no predictive power, so they're dropped. `Exited` is the target.
- **One-hot encoding:** `Geography` (France/Germany/Spain) and `Gender` are text, so they become 0/1 columns with `pd.get_dummies`. `drop_first=True` avoids the dummy-variable trap.
- **Normalization (StandardScaler):** z = (x − mean) / std. It's **fitted on the training data only** to avoid data leakage. Neural networks need it because features like Balance (0–250,000) and HasCrCard (0/1) have very different ranges, and unscaled inputs make gradient descent slow and unstable.
- **Artificial Neural Network (ANN):** layers of neurons. Each neuron computes `activation(w·x + b)`.
  - **ReLU** = max(0, x) in the hidden layers: fast, and avoids vanishing gradients.
  - **Sigmoid** = 1/(1+e⁻ˣ) in the output layer: gives a probability between 0 and 1. If it's > 0.5, the prediction is "will leave".
  - **Binary cross-entropy loss** is used for two-class problems. The **Adam optimizer** is an adaptive-learning-rate version of gradient descent.
  - **Epoch** = one pass over the training data. **Batch size** = samples per weight update.
- **Points of improvement implemented:**
  1. More hidden layers and neurons (6 → 32 + 16) for more learning capacity
  2. **Dropout (20%)**, which randomly disables neurons during training to prevent **overfitting**
  3. **EarlyStopping**, which stops when validation loss hasn't improved for 10 epochs and restores the best weights
  4. More epochs (up to 100) with a tuned Adam learning rate
  Other ideas you can mention: class weights or SMOTE for the imbalance, batch normalization, hyperparameter tuning.
- **Accuracy and confusion matrix:** accuracy alone can mislead with imbalanced data (always predicting "stays" already gives about 80%). That's why the confusion matrix and recall for the "Exited" class are also printed.

## Code walkthrough
1. Import pandas, sklearn and Keras (`tensorflow.keras`), and set a random seed for reproducibility.
2. Read the CSV, check for nulls and plot the class balance.
3. Drop the ID columns, one-hot encode, then do a stratified 80/20 split.
4. Fit `StandardScaler` on the train set and transform both sets.
5. **Basic model:** `Sequential([Input, Dense(6, relu), Dense(1, sigmoid)])`, 20 epochs.
6. **Improved model:** `Dense(32) → Dropout → Dense(16) → Dropout → Dense(1)` with `EarlyStopping`. Accuracy and loss curves are plotted.
7. Predict probabilities and threshold at 0.5, then print both accuracies, the confusion matrix and a classification report, and show a heatmap.
