#!/usr/bin/env python3
"""
optimized_checker.py – Ultra-fast key lookup using mmap
"""

import mmap
import os

def key_exists(file_path: str, key: str) -> bool:
    """Return True if key exists in file using memory-mapped I/O."""
    if not key:
        return False

    key_bytes = key.encode("utf-8")
    try:
        filesize = os.path.getsize(file_path)
        if filesize == 0:
            return False
    except OSError:
        return False

    try:
        with open(file_path, "rb") as f:
            with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as mm:
                return mm.find(key_bytes) != -1
    except (OSError, ValueError):
        with open(file_path, "rb") as f:
            return key_bytes in f.read()