import csv

from datasets import load_dataset

ds = load_dataset("puyang2025/seven-phishing-email-datasets")
print(ds)

train_data = ds["train"]
print(train_data)

# Here we are previewing the first 3 rows so we can have a picture of the structure of dataset
for i in range(3):
    print(train_data[i])
    print("--------------------------------")

columns = ['text', 'subject', 'label', 'sender', 'receiver', 'date', 'urls', 'dataset_name']

# Checking each column and count how many missing values it has
for col in columns:
    missing = 0
    for row in train_data:
        if row[col] is None:
            missing += 1
    print(col, "missing:", missing)


# Here we are keeping only rows with valid text, subject, and label (0 or 1)
filtered_data = []
for row in train_data:
    if row["text"] is not None and row["subject"] is not None and row["label"] in [0, 1]:
        filtered_data.append(row)

# Keeping only important features (text, subject, label)
clean_data = []
for row in filtered_data:
    clean_row = {
        "text": row["text"],
        "subject": row["subject"],
        "label": row["label"]
    }
    clean_data.append(clean_row)

print(len(clean_data))

# Counting how many samples belong to each label (0 and 1)
count_0 = 0
count_1 = 0

for row in clean_data:
    if row["label"] == 0:
        count_0 += 1
    elif row["label"] == 1:
        count_1 += 1

print("Label 0:", count_0)
print("Label 1:", count_1)

# Calculating the length of each text
for row in clean_data:
    row["text_length"] = len(row["text"])

print(clean_data[0])

# Counting number of words in each email
for row in clean_data:
    row["word_count"] = len(row["text"].split())

# Checking if email contains a link
for row in clean_data:
    if "http" in row["text"]:
        row["has_link"] = 1
    else:
        row["has_link"] = 0

# Count how many exclamation marks (!) are in each email
for row in clean_data:
    row["exclamation_count"] = row["text"].count("!")

print(clean_data[0])

len_0 = 0
len_1 = 0
count_0 = 0
count_1 = 0

# Computing total text length separately for each label
for row in clean_data:
    if row["label"] == 0:
        len_0 += row["text_length"]
        count_0 += 1
    else:
        len_1 += row["text_length"]
        count_1 += 1

print("Avg length label 0:", len_0 / count_0)
print("Avg length label 1:", len_1 / count_1)

link_0 = 0
link_1 = 0

# Counting how many emails contain links 
for row in clean_data:
    if row["label"] == 0:
        link_0 += row["has_link"]
    else:
        link_1 += row["has_link"]

print("Label 0 link %:", link_0 / count_0)
print("Label 1 link %:", link_1 / count_1)

# Counting how many phishing-related keywords appear in each email
keywords = ["urgent", "verify", "password", "account", "click", "login"]

for row in clean_data:
    text_lower = row["text"].lower()
    
    count = 0
    for word in keywords:
        if word in text_lower:
            count += 1
    
    row["keyword_count"] = count

print(clean_data[0])

# Calculating total keyword counts for each label
kw_0 = 0
kw_1 = 0

for row in clean_data:
    if row["label"] == 0:
        kw_0 += row["keyword_count"]
    else:
        kw_1 += row["keyword_count"]

print("Avg keyword count label 0:", kw_0 / count_0)
print("Avg keyword count label 1:", kw_1 / count_1)

# Save cleaned dataset into a CSV file
with open("cleaned_dataset.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=clean_data[0].keys())
    writer.writeheader()
    writer.writerows(clean_data)


# ====================== MODEL TRAINING ======================

import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay


df = pd.read_csv("cleaned_dataset.csv")

# Combine subject and body so the vectorizer sees both
df["full_text"] = df["subject"].astype(str) + " " + df["text"].astype(str)

X = df["full_text"]
y = df["label"]

# stratify keeps the phishing/legit ratio consistent across the split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


print("\n--- Logistic Regression ---")
model_lr = LogisticRegression(max_iter=1000)
model_lr.fit(X_train_tfidf, y_train)
predictions_lr = model_lr.predict(X_test_tfidf)
acc_lr = accuracy_score(y_test, predictions_lr)
print("Accuracy:", acc_lr)
print(classification_report(y_test, predictions_lr, target_names=["Legit", "Phishing"]))


print("\n--- Naive Bayes ---")
model_nb = MultinomialNB()
model_nb.fit(X_train_tfidf, y_train)
predictions_nb = model_nb.predict(X_test_tfidf)
acc_nb = accuracy_score(y_test, predictions_nb)
print("Accuracy:", acc_nb)
print(classification_report(y_test, predictions_nb, target_names=["Legit", "Phishing"]))


if acc_lr >= acc_nb:
    best_model = model_lr
    best_predictions = predictions_lr
    best_name = "Logistic Regression"
else:
    best_model = model_nb
    best_predictions = predictions_nb
    best_name = "Naive Bayes"

print("\nBest model:", best_name)


ConfusionMatrixDisplay.from_predictions(
    y_test, best_predictions, display_labels=["Legit", "Phishing"], cmap="Blues"
)
plt.title("Confusion Matrix - " + best_name)
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.show()


joblib.dump(best_model, "phishing_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
print("Model and vectorizer saved.")


def predict_email(subject, text):
    full = subject + " " + text
    vec = vectorizer.transform([full])
    pred = best_model.predict(vec)[0]
    if pred == 1:
        return "Phishing"
    else:
        return "Legit"


print("\n--- Example predictions ---")
print(predict_email(
    "URGENT: Verify your account now",
    "Click here to verify your password before your account is suspended!"
))
print(predict_email(
    "Meeting tomorrow",
    "Hi team, just a reminder our meeting starts at 10am. Bring your notes."
))