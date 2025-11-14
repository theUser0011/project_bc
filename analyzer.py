# analyzer.py
from typing import List, Dict, Any

def build_address_lookup(data: List[Dict[str, Any]]) -> Dict[str, Dict]:
    """Build O(1) lookup dictionary by address."""
    return {obj["address"]: obj for obj in data}

def categorize_addresses(data: List[Dict]) -> Dict[str, List[Dict]]:
    """Categorize Bitcoin addresses by type."""
    legacy = []
    p2sh = []
    bech32 = []
    taproot = []

    for obj in data:
        addr = obj["address"]
        if addr.startswith("1"):
            legacy.append(obj)
        elif addr.startswith("3"):
            p2sh.append(obj)
        elif addr.startswith("bc1q"):
            bech32.append(obj)
        elif addr.startswith("bc1p"):
            taproot.append(obj)

    print(f"Legacy (1...): {len(legacy)}")
    print(f"P2SH (3...): {len(p2sh)}")
    print(f"Bech32 (bc1q...): {len(bech32)}")
    print(f"Taproot (bc1p...): {len(taproot)}")

    return {"legacy": legacy, "p2sh": p2sh, "bech32": bech32, "taproot": taproot}