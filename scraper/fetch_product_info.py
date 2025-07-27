import requests
from bs4 import BeautifulSoup
import json
import time
import os

API_URL = "https://api.upcitemdb.com/prod/trial/lookup"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Ammo-Catalog-Builder"
}

def fetch_info(upc):
    try:
        response = requests.get(API_URL, params={"upc": upc}, headers=HEADERS, timeout=10)
        data = response.json()

        # Save debug log
        os.makedirs("output", exist_ok=True)
        with open(f"output/debug_{upc}.json", "w", encoding="utf-8") as debug_file:
            json.dump(data, debug_file, indent=2)

        if data.get("code") == "OK" and data.get("total", 0) > 0:
            item = data["items"][0]

            # Title
            raw_title = item.get("title")
            title = raw_title.strip() if raw_title and raw_title.strip() else f"Bulk Ammo – UPC {upc}"

            # Description
            raw_desc = item.get("description")
            if raw_desc:
                soup = BeautifulSoup(raw_desc, "html.parser")
                stripped_desc = soup.get_text(separator=" ", strip=True)
                description = stripped_desc if stripped_desc else f"Ammunition product for UPC {upc}."
            else:
                description = f"Ammunition product for UPC {upc}."

            # Images (use only valid image links)
            images = item.get("images", [])
            image = ""
            for img_url in images:
                try:
                    img_response = requests.get(img_url, stream=True, timeout=5)
                    if img_response.status_code == 200:
                        image = img_url
                        break
                except:
                    continue

            return {
                "title": title,
                "description": description,
                "image_url": image
            }

    except Exception as e:
        print(f"Error fetching info for UPC {upc}: {e}")

    return {
        "title": f"Bulk Ammo – UPC {upc}",
        "description": f"Ammunition product for UPC {upc}.",
        "image_url": ""
    }
