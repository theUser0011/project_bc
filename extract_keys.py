import json
import os
import gc
import sys

JSON_DIR = "./json_files"
OUTPUT_FILE = "all_keys.txt"

def extract_keys_stream():
    total_keys = 0  # count all keys processed

    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:

        files = [f for f in os.listdir(JSON_DIR) if f.endswith(".json")]
        total_files = len(files)
        current_file_index = 1

        for fname in files:

            full_path = os.path.join(JSON_DIR, fname)

            print(f"Reading: {full_path}")

            try:
                with open(full_path, "r", encoding="utf-8") as f:

                    data = json.load(f)
                    keys_list = list(data.keys())
                    num_keys = len(keys_list)

                    for i, key in enumerate(keys_list, start=1):
                        outfile.write(key + "_")

                        # LIVE PROGRESS (one-line updating)
                        sys.stdout.write(
                            f"\033[F\033[KProcessing {i}/{num_keys} keys in file {current_file_index}/{total_files}\n"
                        )
                        sys.stdout.flush()

                    total_keys += num_keys

                # FREE MEMORY
                del data
                gc.collect()

                print(f"✔ Completed file {current_file_index}/{total_files} ({num_keys} keys)")

            except Exception as e:
                print("Error:", e)

            current_file_index += 1

    print("\n🔥 Done! Total keys extracted:", total_keys)
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    extract_keys_stream()
