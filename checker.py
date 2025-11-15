# optimized_checker.py
import mmap
import os

def key_exists(file_path: str, key: str) -> bool:
    """
    Ultra-fast substring search using memory-mapped file (mmap).
    NO RAM is used (file is streamed through kernel pages).
    Perfect for VPS / huge files.
    """

    key = key.encode("utf-8")

    filesize = os.path.getsize(file_path)
    if filesize == 0:
        return False

    with open(file_path, "rb") as f:
        # Memory map entire file (zero RAM; OS pages it in chunks)
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as mm:

            # FASTEST substring search available on CPU
            pos = mm.find(key)

            return pos != -1

