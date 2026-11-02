# LP-III (410246) Practical Codes – SPPU BE Computer (2019 Course)

Runnable code for every practical in the Laboratory Practice III manual that needs code.
Each practical has its own folder with the code, the dataset (where needed), and a `README.md` that explains the concepts, the code and how to run it.

| # | Practical | Language / Tool | Folder |
|---|---|---|---|
| 1 | Fibonacci – recursive and non-recursive | Python | `Practical_01_Fibonacci` |
| 2 | Huffman Encoding (Greedy) | Python | `Practical_02_Huffman_Encoding` |
| 3 | Fractional Knapsack (Greedy) | Python | `Practical_03_Fractional_Knapsack` |
| 4 | 0-1 Knapsack (Dynamic Programming) | Python | `Practical_04_01_Knapsack_DP` |
| 5 | N-Queens with first queen placed (Backtracking) | Python | `Practical_05_N_Queens` |
| 7 | Uber fare prediction (Linear Regression vs Random Forest) | Python `.py` + `.ipynb` | `Practical_07_Uber_Fare_Prediction` |
| 8 | Email spam detection (KNN vs SVM) | Python `.py` + `.ipynb` | `Practical_08_Email_Spam_KNN_SVM` |
| 9 | Bank customer churn (Neural Network) | Python `.py` + `.ipynb` (TensorFlow/Keras) | `Practical_09_Bank_Churn_Neural_Network` |
| 10 | KNN on diabetes.csv | Python `.py` + `.ipynb` | `Practical_10_KNN_Diabetes` |
| 11 | K-Means / Hierarchical clustering + Elbow method | Python `.py` + `.ipynb` | `Practical_11_KMeans_Clustering_Sales` |
| 15 | Bank account smart contract | Solidity (Remix IDE) | `Practical_15_Bank_Smart_Contract` |
| 17 | Business network using Hyperledger | Hyperledger Composer (CTO + JS + ACL) | `Practical_17_Hyperledger_Business_Network` |

**Mini projects included:**
| # | Mini project | Language | Folder |
|---|---|---|---|
| 6 | Matrix multiplication vs multithreaded (thread per row and per cell) | Python | `MiniProject_06_Multithreaded_Matrix_Multiplication` |
| 12 | Titanic survival prediction | Python `.py` + `.ipynb` | `MiniProject_12_Titanic_Survival_Prediction` |

**Not included:**
- 18 (blockchain e-voting dApp mini project).
- 13 (MetaMask installation), 14 (MetaMask wallet) and 16 (survey report on blockchain types) don't need any code. They're installation steps or a written report, and the manual already covers them.

---

## One-time setup (any computer)

### Step 1 – Install Python
You need **Python 3.10, 3.11 or 3.12, 64-bit**. TensorFlow (Practical 9) doesn't support the newest or 32-bit Python versions yet.

- **Windows:** download from https://www.python.org/downloads/windows/. In the installer, **tick "Add python.exe to PATH"**, then click *Install Now*.
- **macOS:** download the macOS installer from https://www.python.org/downloads/macos/, or use `brew install python@3.12`.
- **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install python3 python3-pip python3-venv`

Check that it worked. Open a terminal (on Windows: *Command Prompt* or *PowerShell*) and run:
```bash
python --version      # Windows
python3 --version     # macOS / Linux
```

> On macOS and Linux, use `python3` and `pip3` wherever this guide says `python` and `pip`.

### Step 2 – Open a terminal in this folder
Unzip `LP3_Practicals.zip`, then open a terminal inside the `LP3_Practicals` folder.
- Windows: open the folder in File Explorer, type `cmd` in the address bar and press Enter.
- macOS/Linux: right-click the folder → *Open in Terminal*, or use `cd path/to/LP3_Practicals`.

### Step 3 – Create a virtual environment (recommended)
A virtual environment keeps these libraries separate from the rest of your system.
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```
You'll see `(venv)` at the start of the prompt. Run the activate line again every time you open a new terminal.
*(PowerShell error "running scripts is disabled"? Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use Command Prompt instead.)*

### Step 4 – Install the libraries
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
This installs numpy, pandas, scikit-learn, scipy, matplotlib, seaborn, TensorFlow and Jupyter. TensorFlow is about 500 MB, so the first install takes a few minutes.

**Practicals 1–5 need no libraries.** Plain Python is enough, so you can skip Steps 3–4 if you only need those.

**Using Anaconda instead?** Anaconda already includes everything except TensorFlow. Open *Anaconda Prompt*, `cd` to this folder and run `pip install tensorflow`.

### Step 5 – Run a practical
Always `cd` **into the practical's folder** first, so the program finds its dataset.
```bash
cd Practical_01_Fibonacci
python fibonacci.py
```
For ML practicals you can run either version:
```bash
cd Practical_10_KNN_Diabetes
python knn_diabetes.py               # script: graphs open in windows, close each to continue
jupyter notebook knn_diabetes.ipynb  # notebook: opens in browser → Kernel > Restart & Run All
```
The `.ipynb` files also open directly in **VS Code** (with the Python + Jupyter extensions) or can be uploaded to **Google Colab**. In Colab, also upload the CSV from the same folder using the Files panel on the left.

### What input each practical asks for
Each practical's README has an **Input guide** section with examples and test cases.
| Practical | Input |
|---|---|
| 1 Fibonacci | one integer n, e.g. `10` |
| 2 Huffman | one line of text, e.g. `hello world` |
| 3 Fractional Knapsack | n, then `value weight` on each line, then capacity |
| 4 0-1 Knapsack | n, then `value weight` (integers) on each line, then capacity |
| 5 N-Queens | N, then the column (1..N) of the first queen |
| 7–11 ML | **no input**: reads the CSV in its folder (close each graph window to continue) |
| Mini 6 Matrix | choice 1/2/3, then n, then (choice 2) the matrix rows |
| Mini 12 Titanic | **no input**: reads train.csv/test.csv and writes submission.csv |
| 15 Smart contract | values typed into Remix: deposit uses the VALUE box (Ether), withdraw takes an amount in wei |
| 17 Hyperledger | JSON from `test-data/`, pasted into Playground |

### Blockchain practicals (15, 17)
- **Practical 15:** nothing to install. Open https://remix.ethereum.org in a browser and follow the folder's README.
- **Practical 17:** needs Docker, or Node.js 8. Step-by-step instructions are in its README.

---

## Troubleshooting
| Problem | Fix |
|---|---|
| `'python' is not recognized` (Windows) | Reinstall Python with **"Add to PATH"** ticked, or use `py` instead of `python` |
| `ModuleNotFoundError: No module named 'pandas'` (or similar) | The virtual environment isn't active, or Step 4 wasn't run. Activate `venv` and run `pip install -r requirements.txt` |
| `FileNotFoundError: ... .csv` | You're not inside the practical's folder. `cd` into it first. |
| `No matching distribution found for tensorflow` | Your Python is too new or 32-bit. Install 64-bit Python 3.11/3.12 and recreate the venv. |
| TensorFlow DLL error on Windows | Install the Microsoft Visual C++ Redistributable (x64) and restart |
| Graph windows don't appear (Linux) | `sudo apt install python3-tk` |
| Script seems "stuck" after a graph | It's waiting for you to close the graph window |
| `UnicodeDecodeError` with the sales CSV | Use the given code, which reads it with `encoding="latin1"` |

## Datasets
All datasets are included in their practical folders. They're the same files the manual links on Kaggle:
- `uber.csv`: https://www.kaggle.com/datasets/yasserh/uber-fares-dataset
- `emails.csv`: https://www.kaggle.com/datasets/balaka18/email-spam-classification-dataset-csv
- `Churn_Modelling.csv`: https://www.kaggle.com/barelydedicated/bank-customer-churn-modeling
- `diabetes.csv`: Pima Indians Diabetes dataset (Kaggle)
- `sales_data_sample.csv`: https://www.kaggle.com/datasets/kyanyoga/sample-sales-data
- `train.csv` / `test.csv` (Titanic): https://www.kaggle.com/competitions/titanic/data
