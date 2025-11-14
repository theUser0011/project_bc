# count_keys.py

def count_lines(file_path: str) -> int:
    count = 0
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for _ in f:
            count += 1
    return count


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 count_keys.py <FILE_PATH>")
        exit(1)

    file_path = sys.argv[1]
    print("Counting keys...")

    total = count_lines(file_path)

    print(f"Total keys: {total}")
