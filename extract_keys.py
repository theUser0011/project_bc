import json
import os

# Folder containing your 4 JSON files
FOLDER = "./json_files"

# Output file
OUTPUT_FILE = "all_keys.txt"

all_keys = []

# Loop through all JSON files
for filename in sorted(os.listdir(FOLDER)):
    if filename.endswith(".json"):
        filepath = os.path.join(FOLDER, filename)
        print(f"Reading: {filepath}")
        
        # Load JSON (dictionary)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Collect keys
        all_keys.extend(data.keys())

# Join keys with "_"
result = "_".join(all_keys)

# Save to a single text file
with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write(result)

print("\n✔ All keys saved to", OUTPUT_FILE)
print(f"Total keys collected: {len(all_keys)}")
