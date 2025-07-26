import requests

API_KEY = "your_api_key_here"  # <-- Replace with your UPCItemDB key

def fetch_info(upc):
    url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={upc}"
    headers = {
        "user_key": API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if data["code"] == "OK" and data["total"] > 0:
            item = data["items"][0]
            return {
                "title": item.get("title", f"Ammo - UPC {upc}"),
                "description": item.get("description", f"Ammo product for UPC {upc}."),
                "image_url": item["images"][0] if item["images"] else "https://via.placeholder.com/150"
            }
        else:
            return {
                "title": f"Ammo - UPC {upc}",
                "description": f"Ammo product for UPC {upc}.",
                "image_url": "https://via.placeholder.com/150"
            }

    except Exception as e:
        print(f"Error fetching info for UPC {upc}: {e}")
        return {
            "title": f"Ammo - UPC {upc}",
            "description": f"Ammo product for UPC {upc}.",
            "image_url": "https://via.placeholder.com/150"
        }
