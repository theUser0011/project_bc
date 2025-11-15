#!/usr/bin/env python3
from mnemonic import Mnemonic
from bip_utils import (
    Bip39SeedGenerator,
    Bip44, Bip44Coins, Bip44Changes,
    Bip49, Bip49Coins,
    Bip84, Bip84Coins,
    Bip86, Bip86Coins,
)

def four_addresses(mnemonic_phrase: str, passphrase: str = "") -> list:
    mnemo = Mnemonic("english")          # language check only – seed works for any language
    if not mnemo.check(mnemonic_phrase):
        raise ValueError("Invalid mnemonic")
    seed = Bip39SeedGenerator(mnemonic_phrase).Generate(passphrase)

    def addr(bip_cls, coins):
        return bip_cls.FromSeed(seed, coins)\
            .Purpose().Coin().Account(0)\
            .Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)\
            .PublicKey().ToAddress()

    return [
        addr(Bip44, Bip44Coins.BITCOIN),   # legacy
        addr(Bip49, Bip49Coins.BITCOIN),   # p2sh-segwit
        addr(Bip84, Bip84Coins.BITCOIN),   # bech32
        addr(Bip86, Bip86Coins.BITCOIN),   # taproot
    ]