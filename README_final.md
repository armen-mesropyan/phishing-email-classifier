## Team Members

- Armen Mesropyan
- Serzh Harutyunyan


A simple machine-learning project for detecting whether an email is Legitimate or Phishing.  
The project uses TF-IDF text features and a trained classification model, then provides an easy web interface using Streamlit.

## Technologies Used

- Python
- Streamlit
- Scikit-learn
- TF-IDF Vectorizer
- Logistic Regression
- Joblib
- Pandas
- Matplotlib

## Project Files

```text
phishing-email-classifier/
│
├── app.py                    # Streamlit web application
├── classifier.py             # Loads model and classifies emails
├── train.py                  # Dataset cleaning, training, and evaluation
├── phishing_model.pkl        # Saved trained ML model
├── tfidf_vectorizer.pkl      # Saved TF-IDF vectorizer
├── confusion_matrix.png      # Model evaluation result
├── report.docx               # Final technical report
└── README.md                 # Project documentation
```

## How It Works

1. The dataset is loaded and cleaned.
2. Email subject and body text are combined.
3. Text is converted into numerical features using TF-IDF.
4. Machine learning models are trained and compared.
5. The best model is saved as `phishing_model.pkl`.
6. The Streamlit app loads the saved model and vectorizer.
7. Users enter an email and receive a phishing or legitimate prediction.

## Model Performance

The confusion matrix shows:

- Legitimate emails correctly classified: 16,866
- Phishing emails correctly classified: 14,658
- Legitimate emails classified as phishing: 524
- Phishing emails missed as legitimate: 435

## Installation

Install the required libraries:

```bash
pip install streamlit scikit-learn pandas matplotlib joblib datasets
```

## Run the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal.

## Example Use

Enter an email such as:

```text
Subject: URGENT: Verify your account now

Click here to verify your password before your account is suspended.
```

The system will analyze the text and return whether it is likely phishing or legitimate.

## Conclusion

This project demonstrates how machine learning can be used as a first-level cybersecurity defense tool.  
It is effective for detecting suspicious email patterns, but in real-world use it should be combined with user awareness, email security tools, and safe browsing practices.


