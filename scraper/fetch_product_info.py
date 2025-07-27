
import requests
import json
import os

def fetch_info(upc):
    log_path = "output/upc_failures.log"
    os.makedirs("output", exist_ok=True)

    url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={upc}"
    try:
        resp = requests.get(url)
        data = resp.json()
        if data.get("code") == "OK" and data.get("total", 0) > 0:
            item = data["items"][0]
            for img_url in item.get("images", []):
                try:
                    img_test = requests.head(img_url, timeout=5)
                    if img_test.status_code == 200:
                        return {
                            "title": item["title"] if item.get("title") else f"Bulk Ammo – UPC {upc}",
                            "description": item.get("description", ""),
                            "image_url": img_url
                        }
                except requests.RequestException:
                    continue

        # Log UPCs that returned no results
        with open(log_path, "a") as log_file:
            log_file.write(f"UPC {upc} - NO DATA RETURNED\n")

        return {
            "title": f"Bulk Ammo – UPC {upc}",
            "description": f"Ammo product for UPC {upc}.",
            "image_url": "https://via.placeholder.com/150?text=No+Image"
        }

    except Exception as e:
        # Log UPCs that caused errors
        with open(log_path, "a") as log_file:
            log_file.write(f"UPC {upc} - ERROR: {str(e)}\n")

        return {
            "title": f"Bulk Ammo – UPC {upc}",
            "description": f"Ammo product for UPC {upc}.",
            "image_url": "https://via.placeholder.com/150?text=Error"
        }
