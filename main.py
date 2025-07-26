import pandas as pd
from scraper.fetch_product_info import fetch_info
from generator.generate_catalog import generate_html

input_file = 'data/input.xlsx'
df = pd.read_excel(input_file)

products = []
for _, row in df.iterrows():
    info = fetch_info(row['UPC'])
    products.append({
        "upc": row['UPC'],
        "round_count": row['Round_Count'],
        "price": row['Price'],
        "title": info['title'],
        "image_url": info['image_url'],
        "seo_description": f"{info['description']} Available now at ${row['Price']} for {row['Round_Count']} rounds.",
        "caliber": "9mm"  # Placeholder; replace with real logic if available
    })

html_output = generate_html(products)
with open('output/catalog.html', 'w') as f:
    f.write(html_output)

print("Catalog generated at output/catalog.html")
