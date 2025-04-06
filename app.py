import streamlit as st
import joblib
import pandas as pd
import base64
from feature_extraction import extract_features
from sklearn.preprocessing import LabelEncoder

# Load model
model = joblib.load("phishing_classifier.pkl")

# Set page config
st.set_page_config(page_title="Phishing URL Detector", page_icon="🔒")

# Encode background image to base64
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

background_image = "rm218-bb-07.jpg"
bg_image_base64 = get_base64(background_image)

# Inject CSS with base64 background image
page_bg_img = f"""
<style>
.stApp {{
    background-image: url("data:image/jpeg;base64,{bg_image_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Page content
st.title("🔍 Phishing URL Detector")
st.markdown("Check if a URL is **safe** or **phishing** in seconds.")

# URL input
url_input = st.text_input("Enter a URL to check", placeholder="https://example.com")

if st.button("Analyze"):
    if url_input:
        features = extract_features(url_input)
        features_df = pd.DataFrame([features])

        # Convert categorical columns to numeric (Label Encode)
        for col in features_df.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            features_df[col] = le.fit_transform(features_df[col])

        # Predict
        prediction = model.predict(features_df)[0]

        if prediction == 1:
            st.error("🚨 This URL is **Phishing**! Be cautious.")
        else:
            st.success("✅ This URL is **Legitimate**.")
    else:
        st.warning("Please enter a URL.")
