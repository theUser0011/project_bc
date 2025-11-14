# download.py
import gdown

def download_file(file_id: str, output: str = "data/file.bin"):
    """
    Download a file from Google Drive using gdown.
    """
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output=output, quiet=False)
    print(f"Downloaded to {output}")

if __name__ == "__main__":
    FILE_ID = "109M0r6BP3H8LS2fNNtKl5cVPorXDYz8M"
    download_file(FILE_ID)