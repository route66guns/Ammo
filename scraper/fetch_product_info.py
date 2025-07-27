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

            # === TITLE ===
            title = item.get("title") or ""
            if not title.strip():
                title = item.get("brand", "") + " " + item.get("model", "")
            if not title.strip() and item.get("offers"):
                title = item["offers"][0].get("title", "")
            if not title.strip():
                title = f"Bulk Ammo – UPC {upc}"
            title = title.strip()

            # === DESCRIPTION ===
            raw_desc = item.get("description", "")
            if raw_desc.strip():
                soup = BeautifulSoup(raw_desc, "html.parser")
                description = soup.get_text(separator=" ", strip=True)
            else:
                if title and title != f"Bulk Ammo – UPC {upc}":
                    description = f"{title} is a premium ammunition product known for its reliability."
                else:
                    description = f"Ammunition product for UPC {upc}."

            # === IMAGE ===
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
