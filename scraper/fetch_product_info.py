
import requests
import json
import os
import time
from bs4 import BeautifulSoup

def test_image_url(url):
    try:
        resp = requests.head(url, timeout=5)
        return resp.status_code == 200
    except:
        return False

def google_image_fallback(upc):
    search_url = f"https://www.google.com/search?tbm=isch&q=ammo+UPC+{upc}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        html = requests.get(search_url, headers=headers, timeout=5).text
        soup = BeautifulSoup(html, "html.parser")
        img_tags = soup.find_all("img")
        for img in img_tags:
            src = img.get("src")
            if src and src.startswith("http") and test_image_url(src):
                return src
    except Exception:
        pass
    return None

def fetch_info(upc):
    log_path = "output/upc_failures.log"
    os.makedirs("output", exist_ok=True)
    time.sleep(1.5)  # Delay to avoid API rate limit

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
                if test_image_url(img_url):
                    image_url = img_url
                    break

            if not image_url:
                image_url = google_image_fallback(upc)
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
            image_url = google_image_fallback(upc)
            if not image_url:
                with open(log_path, "a") as log_file:
                    log_file.write(f"UPC {upc} - NO DATA RETURNED\n")
                image_url = f"https://www.google.com/search?tbm=isch&q=ammo+UPC+{upc}"

            return {
                "title": f"Bulk Ammo – UPC {upc}",
                "description": f"Ammunition product for UPC {upc}.",
                "image_url": image_url
            }

    except Exception as e:
        with open(log_path, "a") as log_file:
            log_file.write(f"UPC {upc} - ERROR: {str(e)}\n")
        image_url = google_image_fallback(upc)
        if not image_url:
            image_url = f"https://www.google.com/search?tbm=isch&q=ammo+UPC+{upc}"
        return {
            "title": f"Bulk Ammo – UPC {upc}",
            "description": f"Ammunition product for UPC {upc}.",
            "image_url": image_url
        }
