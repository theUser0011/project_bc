#!/usr/bin/env python3
"""
batch_runner.py – now writes progress every N checks
"""

import sys, argparse, time, signal, os
from pathlib import Path
from batch_generator import mnemonics_at_relative_index
from address_generator import four_addresses
from checker import stream_search

# ----------------------------------------------------------------------
# Config
PROGRESS_EVERY = 100          # write progress every 100 indices
LENGTH = 12                   # fixed for now (can be CLI arg later)
CSV_FILE = None               # will be set from CLI
BATCH = None
PROGRESS_FILE = None

# ----------------------------------------------------------------------
def save_progress(idx: int):
    if PROGRESS_FILE:
        PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_FILE.write_text(str(idx), encoding="utf-8")

def signal_handler(signum, frame):
    print(f"\n[batch{BATCH}] Caught signal {signum}, saving progress {current_idx}...", file=sys.stderr)
    save_progress(current_idx)
    sys.exit(0)

# ----------------------------------------------------------------------
def main():
    global CSV_FILE, BATCH, PROGRESS_FILE, current_idx

    parser = argparse.ArgumentParser()
    parser.add_argument("batch", type=int, choices=[1,2,3,4])
    parser.add_argument("start_index", type=int, help="Starting relative index in batch")
    parser.add_argument("csv_file", help="Path to all_keys.txt or addresses.csv")
    parser.add_argument("length", type=int, nargs="?", default=12, choices=[12,15,18,21,24])
    args = parser.parse_args()

    BATCH = args.batch
    start_idx = args.start_index
    CSV_FILE = Path(args.csv_file)
    LENGTH = args.length
    PROGRESS_FILE = Path("progress") / f"batch{BATCH}.txt"

    # Install signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    if not CSV_FILE.is_file():
        print(f"CSV file not found: {CSV_FILE}", file=sys.stderr)
        sys.exit(1)

    print(f"[batch{BATCH}] Starting from relative index {start_idx} (length={LENGTH})")

    current_idx = start_idx
    found = False

    try:
        while not found:
            # 1. Get one mnemonic per language at this index
            mnemonics = mnemonics_at_relative_index(BATCH, current_idx, LENGTH)

            # 2. Generate all addresses
            all_addrs = set()
            for phrase in mnemonics:
                try:
                    addrs = four_addresses(phrase)
                    all_addrs.update(addrs)
                except:
                    pass  # invalid mnemonic → skip

            if all_addrs:
                # 3. Check CSV
                found = stream_search(CSV_FILE, "", list(all_addrs),
                                      columns=["legacy","p2sh_segwit","bech32","taproot"])

            if found:
                print(f"[batch{BATCH}] HIT at index {current_idx}!")
                print("True")
                save_progress(current_idx + 1)
                break

            # 4. Progress
            current_idx += 1
            if current_idx % PROGRESS_EVERY == 0:
                save_progress(current_idx)
                print(f"[batch{BATCH}] Checked up to index {current_idx}", end="\r")

    except KeyboardInterrupt:
        print(f"\n[batch{BATCH}] Interrupted at {current_idx}")
        save_progress(current_idx)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        save_progress(current_idx)

    # Final save
    save_progress(current_idx)

if __name__ == "__main__":
    # Dynamic import checker (same as before)
    import importlib.util, pathlib
    spec = importlib.util.spec_from_file_location(
        "checker", pathlib.Path(__file__).with_name("checker.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    stream_search = mod.stream_search
    main()