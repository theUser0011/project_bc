#!/usr/bin/env python3
import urllib.request, json, os
from pathlib import Path

BASE = "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039"
LANGUAGES = {
    "english":            "english.txt",
    "french":             "french.txt",
    "italian":            "italian.txt",
    "spanish":            "spanish.txt",
    "japanese":           "japanese.txt",
    "korean":             "korean.txt",
    "chinese_simplified": "chinese_simplified.txt",
    "chinese_traditional":"chinese_traditional.txt",
    "czech":              "czech.txt",
    "portuguese":         "portuguese.txt",
}

OUTDIR = Path("wordlists")
OUTDIR.mkdir(exist_ok=True)

def download(lang, file):
    url = f"{BASE}/{file}"
    path = OUTDIR / f"{lang}.txt"
    if path.exists():
        print(f"{path.name} already present – skipping")
        return
    print(f"Downloading {lang} …")
    req = urllib.request.Request(url, headers={"User-Agent": "python"})
    with urllib.request.urlopen(req, timeout=12) as r, path.open("wb") as f:
        f.write(r.read())

if __name__ == "__main__":
    for lang, file in LANGUAGES.items():
        download(lang, file)
    print("All wordlists ready in ./wordlists/")