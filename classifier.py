import joblib

_model = joblib.load("phishing_model.pkl")
_vectorizer = joblib.load("tfidf_vectorizer.pkl")


def classify_email(email_text, subject=""):
    """
    Classify an email as Phishing or Legitimate.
    Returns a dict with label, confidence, and a short explanation.
    """
    if not email_text or not email_text.strip():
        raise ValueError("Email content cannot be empty.")

    full_text = (subject + " " + email_text).strip()
    vec = _vectorizer.transform([full_text])

    prediction = _model.predict(vec)[0]
    probabilities = _model.predict_proba(vec)[0]
    confidence = float(probabilities[prediction])

    if prediction == 1:
        label = "Phishing"
        explanation = "This email appears suspicious and may be a phishing attempt."
    else:
        label = "Legitimate"
        explanation = "This email looks safe based on its content."

    return {
        "label": label,
        "confidence": confidence,
        "explanation": explanation,
    }