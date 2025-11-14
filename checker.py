# checker.py
import sys

def key_exists(file_path: str, key: str) -> bool:
    """
    Stream-search for a key inside a large text file without loading into RAM.
    Returns True if found, else False.
    """

    key = key.strip()

    # Make sure we catch keys that are cut between 2 chunks
    carry_over = ""

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        while True:
            chunk = f.read(1024 * 1024)  # 1 MB chunk
            
            if not chunk:
                break

            # Combine last part of previous chunk + current chunk
            combined = carry_over + chunk

            # Check if key exists
            if key in combined:
                return True

            # Save last 100 characters to detect boundary matches
            carry_over = combined[-100:]

    return False


# if __name__ == "__main__":

#     if len(sys.argv) != 3:
#         print("Usage: python checker.py <FILE_PATH> <KEY>")
#         exit(1)

#     file_path = sys.argv[1]
#     key = sys.argv[2]

#     found = key_exists(file_path, key)

#     print(found)
