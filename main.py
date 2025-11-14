# main.py
from download import download_file
from converter import convert_bin_to_json
from analyzer import build_address_lookup, categorize_addresses
from bip39_utils import export_bip39_wordlists, generate_addresses_from_mnemonic
from checker import get_address_info

def main():
    print("Starting Bitcoin Wallet Checker Pipeline...\n")

    # Step 1: Download .bin file
    print("1. Downloading file.bin from Google Drive...")
    download_file("109M0r6BP3H8LS2fNNtKl5cVPorXDYz8M")

    # Step 2: Convert to JSON
    print("\n2. Converting .bin to JSON...")
    data = convert_bin_to_json()

    # Step 3: Build lookup & analyze
    print("\n3. Building address lookup...")
    address_lookup = build_address_lookup(data)

    print("\n4. Categorizing addresses...")
    categorize_addresses(data)

    # Example lookup
    example_addr = "34xp4vRoCGJym3xA7yCVPFHoCNxv4Twseo"
    if example_addr in address_lookup:
        print(f"\nExample: {example_addr} found in data.")

    # Step 5: Export BIP39 wordlists
    print("\n5. Exporting BIP39 wordlists...")
    wordlists = export_bip39_wordlists()

    # Step 6: Test with a known mnemonic
    print("\n6. Testing with sample mnemonic...")
    sample_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    try:
        results = generate_addresses_from_mnemonic(sample_mnemonic)
        for lang, info in list(results.items())[:2]:  # Show first 2
            if "error" not in info:
                print(f"\n[{lang.upper()}] {info['mnemonic']}")
                print(f"  Legacy: {info['address_legacy_1']}")
                print(f"  Bech32: {info['address_bech32_bc1']}")
                bal = get_address_info(info['address_legacy_1'])
                print(f"  Balance: {bal.get('balance_btc', 'N/A')} BTC")
    except Exception as e:
        print(f"Mnemonic test failed: {e}")

    print("\nPipeline completed!")

if __name__ == "__main__":
    main()