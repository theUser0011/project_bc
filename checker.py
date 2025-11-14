# checker.py
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_address_info(address: str) -> Dict:
    """Scrape Blockchair for balance and transaction count."""
    url = f"https://blockchair.com/bitcoin/address/{address}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return {"address": address, "status": response.status_code}

        soup = BeautifulSoup(response.text, "html.parser")

        # Transaction count
        tx_count = None
        tab = soup.select_one("#tab-history-bitcoin-main")
        if tab:
            match = re.search(r'\((\d[,\d]*)\)', tab.text)
            if match:
                tx_count = int(match.group(1).replace(",", ""))

        # Balance
        balance_btc = None
        balance_elem = soup.select_one(".wb-ba")
        if balance_elem:
            balance_text = balance_elem.text.replace("+", "").replace(",", "").strip()
            try:
                balance_btc = float(balance_text)
            except ValueError:
                pass

        return {
            "address": address,
            "tx_count": tx_count,
            "balance_btc": balance_btc,
            "status": 200
        }
    except Exception as e:
        return {"address": address, "error": str(e), "status": "error"}

def check_multiple_addresses(addresses: List[str], max_workers: int = 10) -> List[Dict]:
    """Check multiple addresses concurrently."""
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(get_address_info, addr): addr for addr in addresses}
        for future in as_completed(futures):
            results.append(future.result())
            print(f"Checked: {future.result()['address']}")
    return results