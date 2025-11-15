#!/usr/bin/env python3
"""
batch_runner.py – BTC Seed Scanner with Telegram Alerts & Progress
"""

import sys
import argparse
import time
import signal
import os
from pathlib import Path
from datetime import datetime

# Local imports
from batch_generator import mnemonics_at_relative_index
from address_generator import four_addresses
from telegram_utils import msg_fun, file_fun  # <-- NEW: Telegram support

# ----------------------------------------------------------------------
# Config
PROGRESS_EVERY = 100
HITS_DIR = Path("hits")
HITS_DIR.mkdir(exist_ok=True)

# Global runtime state
BATCH = None
CSV_FILE = None
LENGTH = None
PROGRESS_FILE = None
current_idx = 0

# ----------------------------------------------------------------------
def save_progress(idx: int):
    """Save current index to progress file."""
    if PROGRESS_FILE:
        PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_FILE.write_text(str(idx), encoding="utf-8")

def save_hit_and_notify(batch: int, rel_index: int, mnemonics: list, matched_address: str):
    """
    Save hit to file + send to Telegram immediately.
    """
    hit_file = HITS_DIR / f"batch{batch}_hit_at_{rel_index}.txt"
    abs_index = (batch - 1) * (2048 ** LENGTH // 4) + rel_index
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S IST')

    lines = [
        f"# BITCOIN SEED HIT!",
        f"# Batch: {batch}",
        f"# Relative Index: {rel_index}",
        f"# Absolute Index: {abs_index}",
        f"# Matched Address: {matched_address}",
        f"# Timestamp: {timestamp}",
        f"# Scanner PID: {os.getpid()}",
        "",
        "=== MNEMONICS (ALL LANGUAGES) ==="
    ]

    for phrase in mnemonics:
        first_word = phrase.split()[0]
        lines.append(f"# {first_word.upper()} (guessed language)")
        lines.append(phrase)
        lines.append("")

    # Save to file
    hit_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nHIT SAVED → {hit_file}")

    # Send to Telegram
    caption = (
        f"<b>BITCOIN SEED HIT!</b>\n"
        f"• Batch: <code>{batch}</code>\n"
        f"• Index: <code>{rel_index}</code>\n"
        f"• Address: <code>{matched_address}</code>\n"
        f"• Time: <code>{timestamp}</code>\n"
        f"• PID: <code>{os.getpid()}</code>"
    )
    file_fun(str(hit_file), caption)
    msg_fun(f"SEED HIT! Check Telegram for file: {hit_file.name}")

def signal_handler(signum, frame):
    """Handle Ctrl+C / SIGTERM."""
    global current_idx
    print(f"\n[batch{BATCH}] Signal {signum} received. Saving progress at index {current_idx}...", file=sys.stderr)
    save_progress(current_idx)
    sys.exit(0)

# ----------------------------------------------------------------------
def main():
    global BATCH, CSV_FILE, LENGTH, PROGRESS_FILE, current_idx

    parser = argparse.ArgumentParser(description="BTC Seed Scanner with Telegram Alerts")
    parser.add_argument("batch", type=int, choices=[1,2,3,4], help="Batch number (1-4)")
    parser.add_argument("start_index", type=int, help="Start from this relative index")
    parser.add_argument("csv_file", help="Path to CSV with known addresses (all_keys.txt)")
    parser.add_argument("length", type=int, nargs="?", default=12, choices=[12,15,18,21,24], help="Mnemonic length")
    args = parser.parse_args()

    BATCH = args.batch
    CSV_FILE = Path(args.csv_file)
    LENGTH = args.length
    PROGRESS_FILE = Path("progress") / f"batch{BATCH}.txt"

    # Setup signal handling
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Validate CSV
    if not CSV_FILE.is_file():
        print(f"CSV file not found: {CSV_FILE}", file=sys.stderr)
        sys.exit(1)

    # Load or initialize progress
    start_idx = args.start_index
    if PROGRESS_FILE.exists():
        try:
            saved = int(PROGRESS_FILE.read_text().strip())
            if saved > start_idx:
                start_idx = saved
                print(f"Resuming from saved progress: {start_idx}")
        except:
            pass

    current_idx = start_idx
    print(f"[batch{BATCH}] Starting scan from index {current_idx} | length={LENGTH}")

    try:
        while True:
            # 1. Generate mnemonics (all languages)
            mnemonics = mnemonics_at_relative_index(BATCH, current_idx, LENGTH)

            # 2. Generate addresses + reverse map
            all_addrs = set()
            addr_to_mnemonic = {}

            for phrase in mnemonics:
                try:
                    addrs = four_addresses(phrase)
                    for addr in addrs:
                        all_addrs.add(addr)
                        addr_to_mnemonic[addr] = phrase
                except Exception as e:
                    pass  # Invalid mnemonic → skip

            # 3. Check each address
            matched_addr = None
            for addr in all_addrs:
                if stream_search(CSV_FILE, addr, ["legacy", "p2sh_segwit", "bech32", "taproot"]):
                    matched_addr = addr
                    break

            if matched_addr:
                print(f"\nHIT at index {current_idx}! Address: {matched_addr}")
                winning_phrase = addr_to_mnemonic[matched_addr]
                print(f"Winning mnemonic: {winning_phrase}")

                # Save + notify
                save_hit_and_notify(BATCH, current_idx, mnemonics, matched_addr)
                print("True")
                save_progress(current_idx + 1)
                break

            # 4. Progress
            current_idx += 1
            if current_idx % PROGRESS_EVERY == 0:
                save_progress(current_idx)
                print(f"[batch{BATCH}] Checked → {current_idx}", end="\r", flush=True)

    except KeyboardInterrupt:
        print(f"\n[batch{BATCH}] Interrupted by user at index {current_idx}")
    except Exception as e:
        print(f"\n[batch{BATCH}] Unexpected error: {e}", file=sys.stderr)
        msg_fun(f"Scanner CRASH in batch {BATCH}: {e}")
    finally:
        save_progress(current_idx)
        print(f"\n[batch{BATCH}] Progress saved: {current_idx}")

# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Dynamic import checker
    import importlib.util
    import pathlib

    checker_path = pathlib.Path(__file__).with_name("checker.py")
    spec = importlib.util.spec_from_file_location("checker", checker_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    stream_search = mod.stream_search

    # Dynamic import telegram_utils
    tg_path = pathlib.Path(__file__).with_name("telegram_utils.py")
    if tg_path.exists():
        tg_spec = importlib.util.spec_from_file_location("telegram_utils", tg_path)
        tg_mod = importlib.util.module_from_spec(tg_spec)
        tg_spec.loader.exec_module(tg_mod)
        globals()["msg_fun"] = tg_mod.msg_fun
        globals()["file_fun"] = tg_mod.file_fun
    else:
        # Fallback: dummy functions if telegram_utils not present
        def msg_fun(m): print("Telegram disabled:", m)
        def file_fun(f, c=""): print("File send disabled:", f)

    main()