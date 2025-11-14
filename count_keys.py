# count_keys.py

def count_keys(file_path: str) -> int:
    total = 0
    chunk_size = 1024 * 1024  # 1MB per chunk

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            total += chunk.count("_")

    return total


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 count_keys.py <FILE_PATH>")
        exit(1)

    file_path = sys.argv[1]
    print("Counting keys... (may take 10–30 seconds)")

    total_keys = count_keys(file_path)

    print(f"Total keys: {total_keys}")
