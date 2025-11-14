import os
import json
import psutil
import time
import sys

JSON_FOLDER = "json_files"

def get_memory_usage():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss / (1024 * 1024)  # Convert to MB

def print_system_memory():
    mem = psutil.virtual_memory()
    print(f"\n=== SYSTEM MEMORY ===")
    print(f"Total RAM       : {mem.total / (1024*1024):.2f} MB")
    print(f"Available RAM   : {mem.available / (1024*1024):.2f} MB")
    print(f"Used RAM        : {mem.used / (1024*1024):.2f} MB")
    print(f"Free RAM        : {mem.free / (1024*1024):.2f} MB")
    print("======================\n")

def load_json_files():
    files = [f for f in os.listdir(JSON_FOLDER) if f.endswith(".json")]
    print(f"Found {len(files)} JSON files.\n")

    data = []  # store loaded JSONs
    for idx, file in enumerate(files, start=1):
        file_path = os.path.join(JSON_FOLDER, file)

        print(f"➡ Loading {file} ...")
        start_mem = get_memory_usage()

        try:
            with open(file_path, "r") as f:
                content = json.load(f)
                data.append(content)
        except Exception as e:
            print(f"❌ Failed to load {file}: {e}")
            continue

        end_mem = get_memory_usage()
        print(f"   Memory before load: {start_mem:.2f} MB")
        print(f"   Memory after load : {end_mem:.2f} MB")
        print(f"   Memory increased  : {end_mem - start_mem:.2f} MB\n")

        time.sleep(1)

    print("✔ Finished loading all files.")
    return data

if __name__ == "__main__":
    print_system_memory()

    print("=== STARTING JSON LOAD TEST ===")
    before = get_memory_usage()
    print(f"Process memory before loading: {before:.2f} MB\n")

    data = load_json_files()

    after = get_memory_usage()
    print(f"Process memory after loading: {after:.2f} MB")
    print(f"\nTotal increase after loading all JSONs: {after - before:.2f} MB\n")

    print_system_memory()
