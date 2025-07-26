
import requests

def fetch_info(upc):
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
                            "title": item["title"] if item.get("title") else f"Generic Ammo ({upc})",
                            "description": item.get("description", ""),
                            "image_url": img_url
                        }
                except requests.RequestException:
                    continue
        return {
            "title": f"Generic Ammo ({upc})",
            "description": f"Ammo product for UPC {upc}.",
            "image_url": "https://via.placeholder.com/150?text=No+Image"
        }
    except Exception as e:
        print(f"Error fetching UPC {upc}: {e}")
        return {
            "title": f"Generic Ammo ({upc})",
            "description": f"Ammo product for UPC {upc}.",
            "image_url": "https://via.placeholder.com/150?text=Error"
        }
