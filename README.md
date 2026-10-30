[README.md](https://github.com/user-attachments/files/34192185/README.md)

# 🔐 Intelligent Password Security Analyzer

A machine-learning-powered password strength analyzer that goes beyond static rules. It combines a character-level n-gram TF-IDF model with OWASP-based rule checks and presents everything in an interactive Streamlit app.

> Capstone-I project, Hybrid UG Program in Computer Science & Data Analytics, IIT Patna.

---

## 📌 Overview

Traditional password meters only check composition rules (length ≥ 8, one digit, one uppercase letter). A password like `Password123!` passes all of them yet is trivial to crack with hybrid dictionary attacks. Length and symbols measure *compliance*, not *resistance*.

This project trains a classifier directly on real password data so it can learn the character patterns that make a password weak or strong, then pairs it with rule-based checks and actionable suggestions.

**The model classifies every password into one of three classes:**

| Label | Strength |
|-------|----------|
| 0 | Weak |
| 1 | Medium |
| 2 | Strong |

## ✨ Features

- **ML-based strength prediction** using character n-gram TF-IDF + Logistic Regression
- **Rule-based vulnerability assessment** aligned with OWASP authentication guidelines
- **Actionable recommendations** to improve a weak password
- **Dataset analytics** with label-distribution and comparative visualizations
- **Interactive Streamlit UI** for real-time password analysis
- **Fast inference**: the model is pre-trained and served from serialized artifacts, so no retraining at runtime
- **Test and validation module** covering each component and the integrated app

## 🧩 Project Modules

| Module | Description |
|--------|-------------|
| 1. Password Security Analysis | OWASP research, predictable-pattern analysis, rule-based checker, security suggestions |
| 2. Machine Learning | Data curation, TF-IDF vectorization, model training/evaluation, artifact serialization |
| 3. Data Analytics | Dataset profiling, label-distribution analytics, visualizations |
| 4. UI & Integration | Streamlit interface and integration of all modules |
| 5. Testing & Validation | Test plans, test cases, integration testing, issue tracking |

## 🧠 How the ML Module Works

1. **Dataset**: Kaggle *Password Strength Classification* dataset; a random sample of 50,000 passwords (`random_state=42`).
2. **Preprocessing**: malformed lines skipped, missing values dropped, passwords cast to `str` (prevents numeric-only passwords being read as numbers).
3. **Feature engineering**: `TfidfVectorizer(analyzer="char", ngram_range=(1, 3))`, producing **48,222** character n-gram features. Character-level tokens capture digit runs, repeated characters, keyboard walks, and common suffixes that word tokenizers miss.
4. **Model**: Multinomial Logistic Regression (`max_iter=1000`), chosen for speed on sparse high-dimensional data, near-instant inference, and interpretable weights.
5. **Split**: 80% train (40,000) / 20% test (10,000).

### Inference pipeline

```
Password (Streamlit UI)
      │
      ▼
tfidf_vectorizer.pkl   →  char 1–3-gram TF-IDF
      │
      ▼
password_model.pkl     →  Logistic Regression
      │
      ▼
ml_service.py          →  Class 0 / 1 / 2 returned to the UI
```

## 📊 Results

Evaluated on the 10,000-sample held-out test set:

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| 0 (Weak) | 0.85 | 0.79 | 0.82 | 1,351 |
| 1 (Medium) | 0.89 | 0.94 | 0.91 | 7,419 |
| 2 (Strong) | 0.79 | 0.65 | 0.71 | 1,230 |
| **Accuracy** | | | **0.88** | 10,000 |
| Macro avg | 0.84 | 0.79 | 0.81 | 10,000 |
| Weighted avg | 0.87 | 0.88 | 0.88 | 10,000 |

**Takeaways**
- ~**88% overall accuracy** with a lightweight baseline model.
- The dataset is imbalanced (Medium ≈ 74%, Weak ≈ 13.5%, Strong ≈ 12.3%), which lowers recall on the Strong class.
- Extreme errors are rare: only 12 Weak → Strong and 13 Strong → Weak. Most mistakes are between neighbouring classes.

## 🛠️ Tech Stack

- **Language**: Python
- **ML / Data**: scikit-learn, pandas, joblib
- **Interface**: Streamlit
- **Dataset**: Kaggle Password Strength Classification

## 🚀 Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/<sarvshreshth10>/<Intelligent password strength analyzer>.git
cd <Intelligent-password-strength-analyser>

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install scikit-learn pandas joblib streamlit

# 4. Run the app
streamlit run app.py
```

> Update `app.py` to match the name of your Streamlit entry file.

## 📁 Key Files

```
├── password_model.pkl       # Trained Logistic Regression model
├── tfidf_vectorizer.pkl     # Fitted character n-gram TF-IDF vectorizer
├── ml_service.py            # Loads artifacts once, exposes a prediction function
└── app.py                   # Streamlit application
```

## 🔮 Future Work

- Try tree-based models (Random Forest, XGBoost) to better detect the Strong class
- Tune hyperparameters (regularization strength `C`, n-gram range)
- Add handcrafted features: Shannon entropy, case ratios, numeric density
- Run latency and load tests on the integrated UI

## 📚 References

1. Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR, 12, 2825–2830.
2. OWASP Foundation. *Authentication Cheat Sheet.*
3. Kaggle. *Password Strength Classifier Dataset.*
4. McKinney, W. (2010). *Data Structures for Statistical Computing in Python.* Proceedings of the 9th Python in Science Conference.

## 📄 License

sarvshreshthwebservices.pvt.ltd All rights reserved. 
