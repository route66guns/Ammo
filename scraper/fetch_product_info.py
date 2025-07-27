
import requests
import json
import os
import time

def fetch_info(upc):
    log_path = "output/upc_failures.log"
    os.makedirs("output", exist_ok=True)

    time.sleep(1.5)  # Delay added to reduce chance of hitting API rate limits

    url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={upc}"
    try:
        resp = requests.get(url)
        data = resp.json()
        debug_path = f"output/debug_{upc}.json"
        with open(debug_path, "w") as debug_file:
            json.dump(data, debug_file, indent=2)

        if data.get("code") == "OK" and data.get("total", 0) > 0:
            item = data["items"][0]
            title = item.get("title", f"Bulk Ammo – UPC {upc}")
            description = item.get("description", f"Ammunition product for UPC {upc}.")
            image_url = None

            for img_url in item.get("images", []):
                try:
                    img_test = requests.head(img_url, timeout=5)
                    if img_test.status_code == 200:
                        image_url = img_url
                        break
                except requests.RequestException:
                    continue

            if not image_url:
                with open(log_path, "a") as log_file:
                    log_file.write(f"UPC {upc} - NO IMAGE FOUND\n")
                image_url = f"https://www.google.com/search?tbm=isch&q=ammo+UPC+{upc}"

            return {
                "title": title.strip() if title else f"Bulk Ammo – UPC {upc}",
                "description": description.strip(),
                "image_url": image_url
            }

        else:
            with open(log_path, "a") as log_file:
                log_file.write(f"UPC {upc} - NO DATA RETURNED\n")
            return {
                "title": f"Bulk Ammo – UPC {upc}",
                "description": f"Ammunition product for UPC {upc}.",
                "image_url": f"https://www.google.com/search?tbm=isch&q=ammo+UPC+{upc}"
            }

    except Exception as e:
        with open(log_path, "a") as log_file:
            log_file.write(f"UPC {upc} - ERROR: {str(e)}\n")
        return {
            "title": f"Bulk Ammo – UPC {upc}",
            "description": f"Ammunition product for UPC {upc}.",
            "image_url": f"https://www.google.com/search?tbm=isch&q=ammo+UPC+{upc}"
        }
