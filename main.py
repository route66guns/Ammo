
import pandas as pd
from scraper.fetch_product_info import fetch_info
from generator.generate_catalog import generate_html
from seo_description_builder import build_seo_description
from caliber_detector import detect_caliber_from_title
from title_cleaner import clean_title
import os

os.makedirs('output', exist_ok=True)
df = pd.read_excel('data/input.xlsx')

products = []
for _, row in df.iterrows():
    info = fetch_info(row['UPC'])
    raw_caliber = row.get("Caliber")
    caliber = raw_caliber if pd.notna(raw_caliber) else detect_caliber_from_title(info["title"])
    cleaned_title = clean_title(info["title"])
    seo_description = build_seo_description(
        cleaned_title,
        caliber,
        row["Round_Count"],
        row["Price"]
    )
    products.append({
        "upc": row["UPC"],
        "round_count": int(row["Round_Count"]) if row["Round_Count"] == int(row["Round_Count"]) else row["Round_Count"],
        "price": float(row["Price"]),
        "caliber": caliber,
        "title": cleaned_title,
        "image_url": info["image_url"],
        "seo_description": seo_description
    })

html_output = generate_html(products)
with open('output/catalog.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

print("Catalog generated at output/catalog.html")
