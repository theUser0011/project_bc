import gdown
import os

# Create folder if not exists
folder = "json_files"
os.makedirs(folder, exist_ok=True)

file_ids = [
    "199D5Q2ct4WhmePDPg9cFoQhkI74Sgnv0",
    "1uTLgYT3z5SM0c3eC3nObNbDrBT4bG6kG",
    "1b9bqRW2POpMjIBMsbL5SlEBKOBGHPgdG",
    "1cnZXfuAp5rYYjsVcYX0PXy7ecQEsUlbg"
]

for fid in file_ids:
    url = f"https://drive.google.com/uc?id={fid}"
    output = os.path.join(folder, f"{fid}.json")
    print(f"Downloading {output} ...")
    gdown.download(url, output, quiet=False)

print("✔ All downloads completed into json_files/ folder!")
