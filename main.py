
import pandas as pd
from scraper.fetch_product_info import fetch_info
from generator.generate_catalog import generate_html
from seo_description_builder import build_seo_description
import os

# Ensure output directory exists
os.makedirs('output', exist_ok=True)

# Read input Excel file
input_file = 'data/input.xlsx'
df = pd.read_excel(input_file)

# Generate product list
products = []
for _, row in df.iterrows():
    info = fetch_info(row['UPC'])
    caliber = row.get("Caliber", "N/A")
    seo_description = build_seo_description(
        info["title"],
        caliber,
        row["Round_Count"],
        row["Price"]
    )
    products.append({
        "upc": row["UPC"],
        "round_count": row["Round_Count"],
        "price": row["Price"],
        "caliber": caliber,
        "title": info["title"],
        "image_url": info["image_url"],
        "seo_description": seo_description
    })

# Generate and save HTML
html_output = generate_html(products)
with open('output/catalog.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

print("Catalog generated at output/catalog.html")
