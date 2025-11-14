import json
import os
import gc   # garbage collector

JSON_DIR = "./json_files"
OUTPUT_FILE = "all_keys.txt"

def extract_keys_stream():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:

        for fname in os.listdir(JSON_DIR):
            if not fname.endswith(".json"):
                continue

            full_path = os.path.join(JSON_DIR, fname)
            print("Reading:", full_path)

            try:
                with open(full_path, "r", encoding="utf-8") as f:

                    data = json.load(f)

                    for key in data.keys():
                        outfile.write(key + "_")

                # 🔥 Free memory immediately
                del data
                gc.collect()  # force garbage collector

            except Exception as e:
                print("Error:", e)

    print("✅ Done. Keys saved into", OUTPUT_FILE)


if __name__ == "__main__":
    extract_keys_stream()
