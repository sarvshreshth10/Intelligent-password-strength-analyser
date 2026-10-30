INTELLIGENT PASSWORD SECURITY
ANALYZER USING MACHINE LEARNING AND
DATA ANALYTICS
Capstone-I project report submitted
by the student of
Hybrid UG program in Computer Science & Data Analytics
Student Name: SARV SHRESHTH
Roll No.: US2603CDH90
Group No.: 46
INDIAN INSTITUTE OF TECHNOLOGY PATNA
BIHTA - 801106, INDIA
Date: October 30, 2026
￼1
Declaration
I hereby declare that this submission is my own work and that, to the best of our
knowledge and belief, it contains no material previously published or written by another
person nor material which to a substantial extent has been accepted for the award of any
other degree or diploma of the university or other institute of higher learning, except
where due acknowledgment has been made in the text.
Date: October 30, 2026
Student Name: SARV SHRESHTH
Roll No.: US2603CDH90
Group No.: 46
￼2
Summary of the Project
Authentication mechanisms across modern computing systems rely on textual passwords
as the primary access barrier. Conventional rule-based evaluators verify only syntactic
constraints, such as minimum length or the inclusion of particular character classes, and
therefore fail against predictable patterns and dictionary-based attacks.
The Intelligent Password Security Analyzer is an end-to-end framework that combines
rule-based vulnerability assessment, character-level statistical modelling, dataset
analytics, an interactive Streamlit interface and a testing and validation module. The
system predicts password strength as Weak (0), Medium (1) or Strong (2) using machine
learning, validates passwords against OWASP guidelines, and generates actionable
recommendations.
Work done by each member:
Member Module Work Done / Contributions
Member 1 Module 1: Password
Security Analysis
Research on OWASP criteria, analysis of predictable
password structures, rule-based checker
implementation and security suggestions.
Member 2
(Author)
Module 2: Machine
Learning
Dataset curation, missing-value handling, character n-
gram TF-IDF vectorization, baseline Logistic
Regression training, performance evaluation and
artifact serialization (password_model.pkl,
tfidf_vectorizer.pkl, ml_service.py).
Member 3 Module 3: Data
Analytics
Dataset profiling, label-distribution analytics,
comparative visualizations and statistical interpretation
of classifier output.
Member 4 Module 4: User Interface
and Integration
Streamlit application interface (password input,
security result, suggestions and analytics sections) and
integration of all modules into one usable application.
Member 5 Module 5: Testing,
Evaluation and Security
Validation
Test-plan and test-case design, verification of each
module's expected behaviour, testing of the integrated
application, and documentation of results, issues and
fixes.
￼3
Contents
Chapter 1: Introduction 5 ..................................................................................................
1.1 Background & Motivation 5 .....................................................................................
1.2 Problem Statement 5 .................................................................................................
1.3 Project Objectives 5 ..................................................................................................
1.4 Literature Review / Existing Approaches 5 ..............................................................
Chapter 2: Proposed Methodology & Implementation 6 ................................................
2.1 Dataset Description & Class Distribution 6 ..............................................................
2.2 Data Cleaning & Preprocessing 6 .............................................................................
2.3 Feature Engineering (Character n-gram TF-IDF) 6 ..................................................
2.4 Model Selection & Training 6 ...................................................................................
2.5 Experimental Results & Evaluation 7 .......................................................................
2.6 Artifact Serialization & Integration Architecture 7 ...................................................
Chapter 3: Conclusion & Future Work 9 .........................................................................
3.1 Summary of Mid-Term Progress 9 ...........................................................................
3.2 Future Work Plan (For Final Submission, 30 December 2026) 9 .............................
References 10 .......................................................................................................................
￼4
Chapter 1: Introduction
1.1 Background & Motivation
Single-factor textual authentication remains ubiquitous in personal and enterprise
systems. Human memorization bias, however, leads users to choose common dictionary
words, simple character substitutions (for example @ for a), keyboard walks (qwerty)
and sequential suffixes (12345). Traditional password strength meters enforce static
rules such as a minimum of eight characters, one digit and one uppercase letter. A
password such as Password123! satisfies these rules yet offers negligible resistance to
modern hybrid dictionary and rule-based cracking attacks.
Length and symbol rules measure compliance, not resistance. Machine learning allows a
classifier to learn character-level co-occurrences and structural patterns directly from
real password corpora, giving a far more realistic estimate of strength.
1.2 Problem Statement
Standard web password checkers lack adaptive, machine-learning-driven evaluation.
They show two main failure modes:
• False positives: structurally trivial but rule-compliant passwords are labelled
"Strong".
• Computational cost: dictionary-based checks need large word lists on the client,
adding latency.
A lightweight statistical model that can classify arbitrary strings with near-instant
inference is needed.
1.3 Project Objectives
• Build an intelligent classifier that categorizes password strength into 0 (Weak), 1
(Medium) and 2 (Strong).
• Combine ML pattern recognition with rule-based security checks, interactive
analytics and systematic testing of the integrated application.
• Represent passwords with a character-level n-gram TF-IDF feature space that
preserves contiguous sub-string patterns.
• Decouple inference from training through serialized artifacts (.pkl files) and a
service wrapper (ml_service.py) for the Streamlit front-end.
1.4 Literature Review / Existing Approaches
Traditional approaches rely on regular expressions and static blacklists: a password is
accepted if it matches composition rules and does not appear in a list of known weak
passwords. These methods are simple and transparent but brittle. They cannot generalize
to unseen variants such as "P@ssw0rd2026", and large blacklists are expensive to ship
and search.
Statistical NLP-style approaches instead tokenize passwords into character n-grams and
learn weights for the sub-strings that indicate weak or strong choices. This captures
￼5
recurring patterns without an explicit dictionary. This project follows this approach and
adds rule-based OWASP checks.
￼6
Chapter 2: Proposed Methodology &
Implementation
This chapter documents Module 2, the Machine Learning Module (Member 2).
2.1 Dataset Description & Class Distribution
The Kaggle Password Strength Classification dataset was used. It contains raw password
strings paired with an integer strength label: Class 0 (Weak), Class 1 (Medium) and
Class 2 (Strong). To keep training fast and memory-safe, a random sample of 50,000
records was drawn (random_state = 42). The class breakdown of the sample is:
Class Samples Share of sample
0 (Weak) 6,756 13.51%
1 (Medium) 37,096 74.19%
2 (Strong) 6,148 12.30%
Total 50,000 100%
Table 2.1: Class distribution of the 50,000-sample dataset
The sample is strongly skewed towards Class 1, which later affects recall on the
minority classes.
2.2 Data Cleaning & Preprocessing
• Malformed lines in the source CSV were skipped while parsing using
pd.read_csv(..., on_bad_lines="skip").
• Rows with missing values were removed with Pandas .dropna().
• Passwords were cast to string type with .astype(str), and labels to integers, to
avoid silent numeric casting of purely numeric passwords.
2.3 Feature Engineering (Character n-gram TF-IDF)
Why character-level tokenization. Passwords are not natural-language sentences and
contain no whitespace word boundaries, so standard word tokenizers would treat each
password as a single token and learn nothing about its structure. Setting analyzer="char"
splits each password into overlapping character sequences, so patterns such as digit runs,
repeated characters and common endings become learnable features.
n-gram range. An n-gram range of (1, 3) was used, capturing single characters, bigrams
(e.g. "er", "12") and trigrams (e.g. "ing", "!@#", "890"). Each n-gram is weighted by
TF-IDF:
TF-IDF(t, d) = TF(t, d) × IDF(t), IDF(t) = ln((1 + N) / (1 + df(t))) + 1
Feature matrix. Applying the vectorizer to the 50,000 passwords produced a sparse
matrix of shape 50,000 × 48,222, i.e. 48,222 unique character n-gram features.
2.4 Model Selection & Training
￼7
Multinomial Logistic Regression (max_iter = 1000) was chosen as the baseline classifier
because:
• it converges quickly and handles high-dimensional sparse matrices efficiently;
• inference is instantaneous, which suits real-time use inside a web interface;
• its learned weights are interpretable and the model file is small.
For K = 3 classes, the class probability is given by the softmax function:
P(y = k | x) = exp(w_k · x + b_k) / Σ_j exp(w_j · x + b_j)
The data were split 80% training (40,000 samples) and 20% testing (10,000 samples)
with random_state = 42. The model was fitted with scikit-learn's LogisticRegression on
the TF-IDF training matrix.
2.5 Experimental Results & Evaluation
The model was evaluated on the 10,000 held-out passwords. The classification report is
shown in Table 2.2 and the confusion matrix in Table 2.3.
Class Precision Recall F1-Score Support
0 (Weak) 0.85 0.79 0.82 1,351
1 (Medium) 0.89 0.94 0.91 7,419
2 (Strong) 0.79 0.65 0.71 1,230
Accuracy 0.88 10,000
Macro avg 0.84 0.79 0.81 10,000
Weighted avg 0.87 0.88 0.88 10,000
Table 2.2: Classification report on the 10,000-sample test set
Predicted 0 Predicted 1 Predicted 2
Actual 0 (Weak) 1,067 272 12
Actual 1 (Medium) 175 6,974 270
Actual 2 (Strong) 13 417 800
Table 2.3: Confusion matrix
Observations. The model reaches an overall accuracy of about 88%. Class 1 (Medium)
has the best F1-score (0.91, recall 94%). Class 2 (Strong) has the weakest recall (0.65),
mainly because of class imbalance. Errors between the extremes are rare: only 12 Weak
passwords were predicted as Strong and 13 Strong as Weak, so most mistakes fall
between neighbouring classes.
2.6 Artifact Serialization & Integration Architecture
After training, the fitted objects were exported with joblib so that the user interface
never has to retrain the model:
• password_model.pkl stores the trained Logistic Regression model (weight
matrix of shape 3 × 48,222 and intercepts).
￼8
• tfidf_vectorizer.pkl stores the fitted TF-IDF vectorizer (48,222-feature
vocabulary and IDF weights, analyzer="char", ngram_range=(1, 3)).
A wrapper module, ml_service.py, loads both artifacts once and exposes a single
prediction function. It transforms a password with the saved vectorizer and returns the
predicted class from the saved model. Member 4 imports this module in the Streamlit
app to obtain real-time predictions without any retraining. Member 5 uses the same
interface to test the model outputs against agreed test cases.
Stage Component
1. Input Password entered in Streamlit UI
2. Vectorization tfidf_vectorizer.pkl (char 1–3-gram TF-IDF)
3. Classification password_model.pkl (Logistic Regression)
4. Output Class 0 / 1 / 2 returned via ml_service.py to the UI
Table 2.4: Inference pipeline used by the application
￼9
Chapter 3: Conclusion & Future Work
3.1 Summary of Mid-Term Progress
The dataset pipeline, character-level vectorizer and working baseline model have been
fully implemented and integrated:
1. 2. 3. 4. A 50,000-password sample was acquired, cleaned and profiled.
A character n-gram (1–3) TF-IDF pipeline producing 48,222 features was built.
A Logistic Regression baseline was trained and evaluated, reaching about 88%
test accuracy.
The model and vectorizer were serialized and a service wrapper (ml_service.py)
was provided for integration with the Streamlit interface.
3.2 Future Work Plan (For Final Submission, 30 December 2026)
• Experiment with tree-based models (Random Forest, XGBoost) to improve
detection of the under-represented Strong class.
• Fine-tune hyperparameters (e.g. the regularization strength C and the n-gram
range) and explore handcrafted features such as Shannon entropy, case ratios and
numeric density.
• Conduct latency and load tests on the integrated UI together with Member 4.
• Support Member 5 in testing the model outputs: provide the input and output
format of ml_service.py, and re-test any issues found after fixes.
￼10
References
1. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of
Machine Learning Research, 12, 2825–2830.
2. OWASP Foundation. Authentication Cheat Sheet. Open Web Application
Security Project.
3. 4. Kaggle. Password Strength Classifier Dataset. Kaggle Datasets repository.
McKinney, W. (2010). Data Structures for Statistical Computing in Python.
Proceedings of the 9th Python in Science Conference, 51–56.
￼11
