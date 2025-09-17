import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from urllib.parse import urljoin
from tqdm import tqdm
import time
import os

# Clear console
os.system("cls")

# Intro message
print("="*60)
print("🌤️  WELCOME TO IMD SATELLITE IMAGE VIEWER  🌤️".center(60))
print("="*60)
print("\nThis script will fetch the latest INSAT satellite image from IMD,")
print("and open it in your default image viewer. You can then choose to save it manually.\n")
print("🚀 Starting in 10 seconds...\n")

# Countdown with tqdm
for i in tqdm(range(10, 0, -1), desc="Starting", ncols=100):
    time.sleep(1)

print("\n🔎 Fetching the latest satellite image...\n")

def fetch_latest_satellite_image():
    """Fetch and display the latest IMD satellite image"""
    base_url = "https://mausam.imd.gov.in"
    url = f"{base_url}/imd_latest/contents/satellite.php"
    
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        # Step 1: Fetch page
        print("Connecting to IMD...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Step 2: Parse HTML
        print("Parsing page...")
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Step 3: Find satellite images
        print("Searching for satellite images...")
        img_candidates = []
        img_tags = soup.find_all("img")
        for img in tqdm(img_tags, desc="Scanning images", ncols=100):
            src = img.get("src", "")
            alt = img.get("alt", "").lower()
            if any(keyword in src.lower() or keyword in alt for keyword in ["satellite", "insat", "vis", "ir"]):
                img_candidates.append(img)

        if not img_candidates:
            print("No satellite images found.")
            return None
        
        # Step 4: Download first candidate
        img_tag = img_candidates[0]
        img_url = urljoin(base_url, img_tag["src"])
        print(f"Downloading image from {img_url} ...")
        img_response = requests.get(img_url, headers=headers, timeout=30)
        img_response.raise_for_status()
        
        # Open the image
        img = Image.open(BytesIO(img_response.content))
        img.show()

        print("Image opened successfully. You can save it manually from the viewer.")
        return img

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    fetch_latest_satellite_image()
