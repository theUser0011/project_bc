#!/usr/bin/env python3
"""
log_manager.py – runs as a daemon
- Every 24h: sends all logs to Telegram, then rotates
- Keeps only last 7 days of logs
"""

import time
import os
import glob
from datetime import datetime, timedelta
from pathlib import Path
from telegram_utils import msg_fun, file_fun

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
KEEP_DAYS = 7
SLEEP_SECONDS = 24 * 60 * 60  # 24 hours

def get_log_files() -> list[Path]:
    return [Path(p) for p in glob.glob(str(LOG_DIR / "batch*.log"))]

def rotate_and_send():
    print(f"[{datetime.now()}] Starting daily log rotation...")
    files = get_log_files()
    if not files:
        print("No log files found.")
        return

    # 1. Send each log file
    for log_file in files:
        caption = f"Log: {log_file.name}\nTime: {datetime.now().isoformat()}"
        file_fun(str(log_file), caption)

    # 2. Create rotated archive
    timestamp = datetime.now().strftime("%Y%m%d")
    archive_dir = LOG_DIR / f"archive_{timestamp}"
    archive_dir.mkdir(exist_ok=True)

    for log_file in files:
        archive_path = archive_dir / log_file.name
        log_file.rename(archive_path)
        # Create empty new log
        log_file.touch()

    # 3. Delete old archives
    cutoff = datetime.now() - timedelta(days=KEEP_DAYS)
    for old_dir in LOG_DIR.glob("archive_*"):
        try:
            dir_date = datetime.strptime(old_dir.name.split("_")[1], "%Y%m%d")
            if dir_date < cutoff:
                for f in old_dir.glob("*"):
                    f.unlink()
                old_dir.rmdir()
                print(f"Deleted old archive: {old_dir.name}")
        except:
            pass

    msg_fun(f"Daily log rotation complete. {len(files)} logs sent and archived.")

def daemon():
    print("Log manager daemon started. Will run every 24h.")
    while True:
        try:
            rotate_and_send()
        except Exception as e:
            msg_fun(f"Log manager error: {e}")
        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    daemon()