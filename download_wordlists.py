#!/usr/bin/env python3
import urllib.request
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

def download_once(lang, file):
    """Download file only if not present."""
    url = f"{BASE}/{file}"
    path = OUTDIR / f"{lang}.txt"

    if path.exists() and path.stat().st_size > 0:
        print(f"{path.name} already exists — NOT downloading again.")
        return

    print(f"Downloading {lang} …")
    req = urllib.request.Request(url, headers={"User-Agent": "python"})
    with urllib.request.urlopen(req, timeout=12) as r, path.open("wb") as f:
        f.write(r.read())
    print(f"Downloaded {path.name}")


def load_wordlists():
    """Load all lists into memory as a dictionary."""
    words = {}
    for lang in LANGUAGES:
        path = OUTDIR / f"{lang}.txt"
        if not path.exists():
            raise FileNotFoundError(f"{path} missing. Run downloads first.")

        with path.open("r", encoding="utf-8") as f:
            words[lang] = [w.strip() for w in f.readlines() if w.strip()]

    return words


if __name__ == "__main__":
    for lang, file in LANGUAGES.items():
        download_once(lang, file)

    lists = load_wordlists()
    print("All wordlists loaded successfully!")
