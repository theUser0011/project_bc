import ijson
import os

JSON_DIR = "./json_files"
OUTPUT_ALL_KEYS = "all_keys.txt"

def stream_extract_keys():
    with open(OUTPUT_ALL_KEYS, "w", encoding="utf-8") as outfile:
        
        files = [f for f in os.listdir(JSON_DIR) if f.endswith(".json")]

        for fname in files:
            full_path = os.path.join(JSON_DIR, fname)
            print("Reading:", full_path)

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    # Stream keys from a large JSON object
                    for key in ijson.kvitems(f, ''):
                        outfile.write(key[0] + "_")

                print("✔ Completed:", fname)

            except Exception as e:
                print("Error with", fname, ":", e)

    print("\n🔥 Done. All keys saved to", OUTPUT_ALL_KEYS)

if __name__ == "__main__":
    stream_extract_keys()
