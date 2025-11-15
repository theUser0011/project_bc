import sys
import argparse
from pathlib import Path

from batch_generator import mnemonics_at_relative_index
from address_generator import four_addresses
from checker import check_addresses     # <-- FIXED: import our checker function


def main():
    parser = argparse.ArgumentParser(description="Batch-wise multi-language mnemonic checker")
    parser.add_argument("batch", type=int, choices=[1, 2, 3, 4], help="Batch number (1-4)")
    parser.add_argument("rel_index", type=int, help="Index inside the batch (0 …)")
    parser.add_argument("csv_file", help="Path to the balances CSV file")
    parser.add_argument(
        "length",
        type=int,
        nargs="?",
        default=12,
        choices=[12, 15, 18, 21, 24],
        help="Mnemonic length (default 12)",
    )
    args = parser.parse_args()

    # 1. get one mnemonic per language
    mnemonics = mnemonics_at_relative_index(args.batch, args.rel_index, args.length)
    print(f"Batch {args.batch} | rel-index {args.rel_index} | {len(mnemonics)} languages")

    # 2. generate 4 addresses for *every* mnemonic
    all_addrs = set()
    for phrase in mnemonics:
        try:
            addrs = four_addresses(phrase)
            all_addrs.update(addrs)
        except Exception as e:
            print(f"Warning: Skipping invalid mnemonic: {e}", file=sys.stderr)

    if not all_addrs:
        print("False")
        return

    # 3. stream-search CSV for ANY matching address
    matches = check_addresses(list(all_addrs), csv_file=args.csv_file)

    print("True" if matches else "False")


if __name__ == "__main__":
    main()
