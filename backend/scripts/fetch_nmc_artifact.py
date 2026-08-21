import urllib.request
import ssl
import hashlib
import os
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    "https://www.nmc.org.in/MCIRest/open/getDocument?path=/Documents/Public/Portal/LatestNews/PGMER-2023.pdf",
    "https://www.nmc.org.in/MCIRest/open/getDocument?path=/Documents/Public/Portal/Gazette/PGMER-2023.pdf",
    "https://www.nmc.org.in/MCIRest/open/getDocument?path=/Documents/Public/Portal/GazetteNotification/PGMER%202023.pdf",
    "https://egazette.gov.in/WriteReadData/2023/250982.pdf"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

output_dir = os.path.join(os.path.dirname(__file__), "..", "artifacts", "nmc")
os.makedirs(output_dir, exist_ok=True)
downloaded_file = os.path.join(output_dir, "PGMER_2023_Official_Gazette.pdf")

success = False
downloaded_url = None
downloaded_bytes = None

for url in urls:
    try:
        print(f"Attempting to download from: {url}")
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            data = resp.read()
            if len(data) > 1000 and (data[:4] == b"%PDF" or "pdf" in resp.headers.get("Content-Type", "").lower()):
                print(f"Successfully downloaded PDF ({len(data)} bytes) from {url}")
                with open(downloaded_file, "wb") as f:
                    f.write(data)
                downloaded_bytes = data
                downloaded_url = url
                success = True
                break
            else:
                print(f"Response not a valid PDF. Content-Type: {resp.headers.get('Content-Type')}, Size: {len(data)}")
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")

if not success:
    print("Could not download directly from web endpoints. Checking for local gazette file...")
else:
    sha256_hash = hashlib.sha256(downloaded_bytes).hexdigest()
    print(f"\n--- PROVENANCE DIGEST COMPUTED ---")
    print(f"File: {downloaded_file}")
    print(f"Bytes: {len(downloaded_bytes)}")
    print(f"SHA-256 Digest: {sha256_hash}")
    print(f"Source URL: {downloaded_url}")
