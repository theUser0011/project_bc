#!/usr/bin/env python3
"""
telegram_utils.py – send messages & files to Telegram
"""

import os
import requests
from typing import Optional

def _get_keys() -> tuple[str, str]:
    KEYS = os.getenv("KEYS")
    if not KEYS:
        raise ValueError("Environment variable 'KEYS' not found. Format: BOT_TOKEN_CHAT_ID")
    try:
        BOT_TOKEN, CHAT_ID = KEYS.split("_", 1)
        return BOT_TOKEN, CHAT_ID
    except ValueError:
        raise ValueError("Invalid KEYS format. Use BOT_TOKEN_CHAT_ID")

def msg_fun(message: str) -> dict:
    """Send a text message to Telegram."""
    BOT_TOKEN, CHAT_ID = _get_keys()
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if not data.get("ok"):
            print("Telegram msg failed:", data)
        return data
    except Exception as e:
        print("Telegram msg error:", e)
        return {}

def file_fun(file_path: str, caption: str = "") -> Optional[dict]:
    """Send a file to Telegram."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    BOT_TOKEN, CHAT_ID = _get_keys()
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    try:
        with open(file_path, "rb") as f:
            files = {"document": f}
            data = {"chat_id": CHAT_ID, "caption": caption}
            r = requests.post(url, files=files, data=data, timeout=30)
            result = r.json()
            if not result.get("ok"):
                print("Telegram file failed:", result)
            else:
                print(f"File sent: {file_path}")
            return result
    except Exception as e:
        print("Telegram file error:", e)
        return None