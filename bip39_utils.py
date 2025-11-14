# bip39_utils.py
import os
from mnemonic import Mnemonic
from bip_utils import (
    Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes,
    Bip49, Bip49Coins, Bip84, Bip84Coins, Bip86, Bip86Coins
)
from typing import Dict, List

SUPPORTED_LANGUAGES = [
    "english", "french", "italian", "spanish",
    "chinese_simplified", "chinese_traditional",
    "japanese", "korean", "czech", "portuguese", "russian"
]

def export_bip39_wordlists(output_dir: str = "data/output_lang_files") -> Dict[str, List[str]]:
    """Export all BIP39 wordlists to files and return dict of lists."""
    os.makedirs(output_dir, exist_ok=True)
    wordlists = {}

    for lang in SUPPORTED_LANGUAGES:
        try:
            mnemo = Mnemonic(lang)
            wordlist = mnemo.wordlist

            # Save to file
            with open(f"{output_dir}/{lang}.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(wordlist))

            # Save to dict
            wordlists[lang] = wordlist
            print(f"Saved: {lang}.txt")

        except Exception as e:
            print(f"Error loading {lang}: {e}")

    return wordlists

def generate_addresses_from_mnemonic(english_mnemonic: str) -> Dict[str, Dict]:
    """
    Given an English mnemonic, generate addresses in all languages.
    """
    mnemo_en = Mnemonic("english")
    try:
        indices = [mnemo_en.wordlist.index(w) for w in english_mnemonic.strip().split()]
    except ValueError as e:
        raise ValueError(f"Invalid word in mnemonic: {e}")

    results = {}
    for lang in SUPPORTED_LANGUAGES:
        try:
            mnemo_lang = Mnemonic(lang)
            lang_words = [mnemo_lang.wordlist[i] for i in indices]
            lang_mnemonic = " ".join(lang_words)

            seed = Bip39SeedGenerator(lang_mnemonic).Generate()

            addr_legacy = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)\
                .Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)\
                .PublicKey().ToAddress()

            addr_p2sh = Bip49.FromSeed(seed, Bip49Coins.BITCOIN)\
                .Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)\
                .PublicKey().ToAddress()

            addr_bech32 = Bip84.FromSeed(seed, Bip84Coins.BITCOIN)\
                .Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)\
                .PublicKey().ToAddress()

            addr_taproot = Bip86.FromSeed(seed, Bip86Coins.BITCOIN)\
                .Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)\
                .PublicKey().ToAddress()

            results[lang] = {
                "mnemonic": lang_mnemonic,
                "address_legacy_1": addr_legacy,
                "address_p2sh_3": addr_p2sh,
                "address_bech32_bc1": addr_bech32,
                "address_bech32m_bc1p": addr_taproot,
            }
        except Exception as e:
            results[lang] = {"error": str(e)}

    return results