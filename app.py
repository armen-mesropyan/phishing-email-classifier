import streamlit as st
from classifier import classify_email


st.set_page_config(
    page_title="Phishing Email Detector",
    page_icon="🛡️",
    layout="centered",
)


st.markdown("""
<style>
    .main { padding-top: 2rem; }

    h1 {
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #6b7280;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    .stTextArea textarea, .stTextInput input {
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        font-size: 0.95rem;
    }

    .stButton button {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: background-color 0.2s;
    }
    .stButton button:hover {
        background-color: #1d4ed8;
    }

    .result-card {
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        border-left: 6px solid;
    }
    .result-phishing {
        background-color: #fef2f2;
        border-color: #dc2626;
        color: #7f1d1d;
    }
    .result-safe {
        background-color: #f0fdf4;
        border-color: #16a34a;
        color: #14532d;
    }

    .result-label {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    .result-explanation {
        font-size: 1rem;
        margin-bottom: 0.8rem;
    }
    .confidence {
        font-size: 0.9rem;
        opacity: 0.85;
    }
</style>
""", unsafe_allow_html=True)


st.markdown("# 🛡️ Phishing Email Detector")
st.markdown(
    '<p class="subtitle">Paste an email below and our model will analyze whether it looks suspicious.</p>',
    unsafe_allow_html=True,
)


subject = st.text_input("Subject (optional)", placeholder="e.g. Urgent: Verify your account")

email_text = st.text_area(
    "Email content",
    placeholder="Paste the full email body here...",
    height=250,
)

analyze = st.button("Analyze Email")


def render_result(result):
    is_phishing = result["label"] == "Phishing"
    css_class = "result-phishing" if is_phishing else "result-safe"
    icon = "⚠️" if is_phishing else "✅"
    confidence_pct = f"{result['confidence'] * 100:.1f}%"

    st.markdown(f"""
    <div class="result-card {css_class}">
        <div class="result-label">{icon} {result['label']}</div>
        <div class="result-explanation">{result['explanation']}</div>
        <div class="confidence">Model confidence: <b>{confidence_pct}</b></div>
    </div>
    """, unsafe_allow_html=True)


if analyze:
    if not email_text.strip():
        st.warning("Please paste an email before analyzing.")
    else:
        with st.spinner("Analyzing email..."):
            try:
                result = classify_email(email_text, subject)
                render_result(result)
            except Exception as e:
                st.error(f"Something went wrong: {e}")


st.markdown("<br>", unsafe_allow_html=True)
st.caption("Built for the Cybersecurity course project • Powered by Logistic Regression + TF-IDF")