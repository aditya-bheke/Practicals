# %% [markdown]
# # Practical 9 : Bank Customer Churn Prediction using a Neural Network
# Given a bank customer, build a neural-network classifier that predicts whether they will
# leave the bank (`Exited = 1`) or not (`Exited = 0`) in the next 6 months.
#
# Steps:
# 1. Read the dataset
# 2. Separate the features and the target, and split into training and test sets
# 3. Normalize the train and test data
# 4. Initialize and build the model, identify points of improvement and implement them
# 5. Print the accuracy score and the confusion matrix
#
# Dataset: `Churn_Modelling.csv` (Kaggle - barelydedicated/bank-customer-churn-modeling), kept in this folder.

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

keras.utils.set_random_seed(42)   # reproducible results
print("TensorFlow version:", tf.__version__)

# %% [markdown]
# ## 1. Read the dataset

# %%
df = pd.read_csv("Churn_Modelling.csv")
print("Shape:", df.shape)
print(df.head())
print("\nMissing values:", df.isnull().sum().sum())
print("\nExited counts (1 = left the bank):\n", df["Exited"].value_counts())

sns.countplot(x="Exited", data=df)
plt.title("Customers who stayed (0) vs left (1)")
plt.show()

# %% [markdown]
# ## 2. Features and target, then the train-test split
# * `RowNumber`, `CustomerId` and `Surname` are identifiers with no predictive value, so they are dropped
# * `Geography` and `Gender` are text, so they become numbers through **one-hot encoding**
#   (`drop_first=True` avoids a redundant column)
# * Target `y` = `Exited`

# %%
X = df.drop(columns=["RowNumber", "CustomerId", "Surname", "Exited"])
y = df["Exited"]
X = pd.get_dummies(X, columns=["Geography", "Gender"], drop_first=True, dtype=int)
print("Features used:", list(X.columns))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=42, stratify=y)
print("Train:", X_train.shape, " Test:", X_test.shape)

# %% [markdown]
# ## 3. Normalize the data
# `StandardScaler` transforms each feature to mean 0 and standard deviation 1.
# It is **fitted only on the training data** and then applied to the test data, so no test information leaks into training.
# Neural networks train much faster and more stably on scaled inputs (Balance runs up to ~250000, while HasCrCard is 0/1).

# %%
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)
n_features = X_train_s.shape[1]

# %% [markdown]
# ## 4a. Initialize and build a basic model
# * Input layer -> 1 hidden layer with 6 neurons (ReLU) -> output neuron (Sigmoid gives a probability of leaving)
# * Loss = binary cross-entropy (two classes), Optimizer = Adam

# %%
basic_model = keras.Sequential([
    keras.Input(shape=(n_features,)),
    layers.Dense(6, activation="relu"),
    layers.Dense(1, activation="sigmoid"),
])
basic_model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
basic_model.summary()

history_basic = basic_model.fit(X_train_s, y_train, validation_split=0.2,
                                epochs=20, batch_size=32, verbose=1)

y_pred_basic = (basic_model.predict(X_test_s) > 0.5).astype(int).ravel()
acc_basic = accuracy_score(y_test, y_pred_basic)
print("Basic model test accuracy:", round(acc_basic, 4))

# %% [markdown]
# ## 4b. Points of improvement, implemented
# 1. **More capacity**: two hidden layers (32 and 16 neurons) so the network can learn more complex patterns
# 2. **Dropout**: randomly switches off 20% of neurons during training to reduce **overfitting**
# 3. **More epochs + EarlyStopping**: train for up to 100 epochs, but stop when validation loss stops improving
#    and restore the best weights
# 4. **Tuned learning rate** for the Adam optimizer

# %%
improved_model = keras.Sequential([
    keras.Input(shape=(n_features,)),
    layers.Dense(32, activation="relu"),
    layers.Dropout(0.2),
    layers.Dense(16, activation="relu"),
    layers.Dropout(0.2),
    layers.Dense(1, activation="sigmoid"),
])
improved_model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001),
                       loss="binary_crossentropy", metrics=["accuracy"])
improved_model.summary()

early_stop = keras.callbacks.EarlyStopping(monitor="val_loss", patience=10,
                                           restore_best_weights=True)
history = improved_model.fit(X_train_s, y_train, validation_split=0.2,
                             epochs=100, batch_size=32, callbacks=[early_stop], verbose=1)

# %%
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history["accuracy"], label="train")
plt.plot(history.history["val_accuracy"], label="validation")
plt.title("Accuracy per epoch")
plt.xlabel("Epoch")
plt.legend()
plt.subplot(1, 2, 2)
plt.plot(history.history["loss"], label="train")
plt.plot(history.history["val_loss"], label="validation")
plt.title("Loss per epoch")
plt.xlabel("Epoch")
plt.legend()
plt.show()

# %% [markdown]
# ## 5. Accuracy score and confusion matrix

# %%
y_prob = improved_model.predict(X_test_s).ravel()
y_pred = (y_prob > 0.5).astype(int)

acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
print("Basic model accuracy    :", round(acc_basic, 4))
print("Improved model accuracy :", round(acc, 4))
print("\nConfusion matrix:\n", cm)
print("\n", classification_report(y_test, y_pred, target_names=["Stayed", "Exited"]))

sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Stayed", "Exited"], yticklabels=["Stayed", "Exited"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion matrix (improved model)")
plt.show()
