#!/usr/bin/env python3
import math
from pathlib import Path
from typing import List, Dict

WORDLIST_DIR = Path("wordlists")
WORDLISTS: Dict[str, List[str]] = {}

# Load every language once
for txt in WORDLIST_DIR.glob("*.txt"):
    lang = txt.stem
    WORDLISTS[lang] = [w.strip() for w in txt.read_text(encoding="utf-8").splitlines() if w.strip()]

# ----------------------------------------------------------------------
def mnemonics_at_relative_index(batch: int, rel_index: int, length: int = 12) -> List[str]:
    """
    batch      : 1-4
    rel_index  : 0 … (total_per_batch-1)
    length     : 12,15,18,21,24  (must be the same for every language)
    Returns a list: [english_mnemonic, french_mnemonic, …]
    """
    if batch not in (1,2,3,4):
        raise ValueError("batch must be 1,2,3 or 4")
    if length not in (12,15,18,21,24):
        raise ValueError("length must be 12,15,18,21 or 24")

    # ---- total combinatorial space for ONE language ----
    base = 2048
    total = base ** length

    # ---- 25 % per batch ----
    per_batch = total // 4
    start = (batch-1) * per_batch
    absolute_index = start + rel_index

    if absolute_index >= total:
        raise IndexError("relative index out of range for this batch")

    # ---- compute the mnemonic for *every* language at the same absolute index ----
    result = []
    for lang, words in WORDLISTS.items():
        idx = absolute_index
        phrase = []
        for _ in range(length):
            phrase.append(words[idx % base])
            idx //= base
        phrase.reverse()
        result.append(" ".join(phrase))
    return result
# ----------------------------------------------------------------------