# converter.py
import pickle
import json
from pathlib import Path

def convert_bin_to_json(bin_path: str = "data/file.bin", json_path: str = "data/output.json"):
    """
    Load pickle .bin file and save as formatted JSON.
    """
    Path(json_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(bin_path, "rb") as f:
        data = pickle.load(f)
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Converted {bin_path} → {json_path}")
    return data

if __name__ == "__main__":
    convert_bin_to_json()