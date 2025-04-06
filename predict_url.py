import pickle
import pandas as pd

from feature_extraction import extract_features  # reuse the same function used during training

# Load the trained model
with open("phishing_classifier.pkl", "rb") as f:
    model = pickle.load(f)

# Get URL input
url = input("Enter a URL to check: ")

# Extract features
features = extract_features(url)
features_df = pd.DataFrame([features])

# Predict
prediction = model.predict(features_df)[0]

# Output result
if prediction == 1:
    print("⚠️ Phishing URL detected!")
else:
    print("✅ Legitimate URL.")
