import pandas as pd
from feature_extraction import extract_features
from tqdm import tqdm

# Load original dataset
df = pd.read_csv("D:\\@project\\data\\dataset_phishing.csv")  # Adjust if path changes
urls = df["url"]
labels = df["status"]

# Storage for features
all_features = []

# Extract features with progress bar
for i in tqdm(range(len(urls)), desc="Extracting features"):
    url = urls[i]
    try:
        basic_feats = extract_features(url)
        combined = {**basic_feats, "status": labels[i]}
        all_features.append(combined)
    except Exception as e:
        print(f"❌ Error processing URL {url}: {e}")

# Convert to DataFrame
final_df = pd.DataFrame(all_features)

# Save the dataset
final_df.to_csv("extracted_features.csv", index=False)
print("✅ Feature extraction completed and saved to 'extracted_features.csv'")
