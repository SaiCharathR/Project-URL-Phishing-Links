import pandas as pd
from feature_extraction import extract_all_features
from whois_extractor import extract_whois_features
from tqdm import tqdm

# Load original dataset
df = pd.read_csv("WebpagePhishingDetection.csv")  # Change path if needed
urls = df["url"]
labels = df["status"]

# Storage
all_features = []

# Progress bar
for i in tqdm(range(len(urls))):
    url = urls[i]
    try:
        basic_feats = extract_all_features(url)
        whois_feats = extract_whois_features(url)
        combined = {**basic_feats, **whois_feats, "status": labels[i]}
        all_features.append(combined)
    except Exception as e:
        print(f"Error processing URL {url}: {e}")

# Convert to DataFrame
final_df = pd.DataFrame(all_features)

# Save the dataset
final_df.to_csv("extracted_features.csv", index=False)
print("✅ Feature extraction completed and saved to 'extracted_features.csv'")
