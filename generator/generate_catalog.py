
def generate_html(products):
    import html

    unique_calibers = sorted(set(p['caliber'] for p in products))

    filter_buttons = '<button onclick="filterCaliber(\'all\')">All</button>'
    for cal in unique_calibers:
        safe_cal = html.escape(cal)
        filter_buttons += f'<button onclick="filterCaliber(\'{safe_cal.lower()}\')">{safe_cal}</button>'

    items_html = ""
    for p in products:
        items_html += f"""
        <div class="item" data-caliber="{p['caliber'].lower()}">
            <img src="{p['image_url']}" alt="{html.escape(p['title'])}">
            <div class="item-info">
                <h2>{html.escape(p['title'])}</h2>
                <p>{html.escape(p['seo_description'])}</p>
                <strong>${p['price']} for {p['round_count']} rounds</strong>
            </div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Ammo Catalog</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f9f9f9;
            padding: 20px;
            max-width: 1200px;
            margin: auto;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5rem;
        }}
        #filter-bar {{
            text-align: center;
            margin-bottom: 20px;
        }}
        #filter-bar button {{
            margin: 5px;
            padding: 10px 15px;
            font-size: 1rem;
            border: 1px solid #ccc;
            border-radius: 8px;
            cursor: pointer;
            background-color: white;
        }}
        #filter-bar button:hover {{
            background-color: #eee;
        }}
        .item {{
            display: flex;
            flex-direction: column;
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 10px;
            margin-bottom: 20px;
            padding: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        .item img {{
            max-width: 100%;
            height: auto;
            margin-bottom: 15px;
            border-radius: 8px;
        }}
        .item-info h2 {{
            margin: 0 0 10px;
            font-size: 1.25rem;
            color: #333;
        }}
        .item-info p {{
            font-size: 0.95rem;
            color: #555;
            margin-bottom: 10px;
        }}
        .item-info strong {{
            color: #000;
            font-size: 1rem;
        }}
        @media (min-width: 768px) {{
            .item {{
                flex-direction: row;
                align-items: flex-start;
            }}
            .item img {{
                width: 200px;
                margin-right: 20px;
            }}
            .item-info {{
                flex: 1;
            }}
        }}
    </style>
    <script>
        function filterCaliber(caliber) {{
            const items = document.querySelectorAll('.item');
            items.forEach(item => {{
                if (caliber === 'all' || item.dataset.caliber === caliber) {{
                    item.style.display = 'flex';
                }} else {{
                    item.style.display = 'none';
                }}
            }});
        }}
    </script>
</head>
<body>
    <h1>Ammo Catalog</h1>
    <div id='filter-bar'>{filter_buttons}</div>
    {items_html}
</body>
</html>
"""
