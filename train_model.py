import pandas as pd

# Load dataset while skipping broken lines
print("Loading dataset...")
df = pd.read_csv("data.csv", on_bad_lines="skip")

# Drop any rows with missing passwords
df.dropna(inplace=True)

# Sample 50,000 rows to keep training fast and memory safe
df_sample = df.sample(n=50000, random_state=42)

print("Dataset loaded successfully!")
print("Strength class distribution in sample:")
print(df_sample["strength"].value_counts())
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

print("\nExtracting features using character TF-IDF...")
# Character n-grams from length 1 to 3
vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(1, 3))
X = vectorizer.fit_transform(df_sample["password"].astype(str))
y = df_sample["strength"].astype(int)

print(f"Feature matrix shape: {X.shape}")

# Split 80% for training and 20% for testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("Data split complete (80% train, 20% test).")
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

print("\nTraining Logistic Regression model...")
# Train beginner-friendly multi-class classifier
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
print("Model training complete!")

print("\nEvaluating model performance...")
y_pred = model.predict(X_test)

print("\n--- Classification Report ---")
print(classification_report(y_test, y_pred))

print("--- Confusion Matrix ---")
print(confusion_matrix(y_test, y_pred))
import joblib

print("\nSaving model and vectorizer...")
joblib.dump(model, "password_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
print("Saved 'password_model.pkl' and 'tfidf_vectorizer.pkl' successfully!")