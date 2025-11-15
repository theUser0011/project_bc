# checker.py
# 4. Stream-search CSV for matching BTC addresses

from pathlib import Path
import csv

def check_addresses(addresses, csv_file="balances.csv"):
    """
    Stream-search through the CSV and return matched addresses.
    
    CSV FORMAT EXPECTED:
        address,balance
    """

    csv_path = Path(csv_file)
    if not csv_path.exists():
        print(f"[ERROR] CSV file not found: {csv_path}")
        return []

    addresses_set = set(addresses)   # O(1) lookup
    found = []

    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            try:
                addr, balance = row[0], row[1]
            except IndexError:
                continue

            if addr in addresses_set:
                print(f"[MATCH] {addr} → {balance}")
                found.append((addr, balance))

    return found


# Quick test when running alone
if __name__ == "__main__":
    test_addresses = ["1ExampleAddressA", "1RandomAddress"]
    results = check_addresses(test_addresses, "balances.csv")

    if results:
        print("FOUND:", results)
    else:
        print("No matches found.")
