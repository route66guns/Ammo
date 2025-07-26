def generate_html(products):
    items_html = ""
    for p in products:
        items_html += f"""
        <div class="item" data-caliber="{p['caliber']}">
            <img src="{p['image_url']}" alt="{p['title']}">
            <h2>{p['title']}</h2>
            <p>{p['seo_description']}</p>
            <strong>${p['price']} for {p['round_count']} rounds</strong>
        </div>
        """
    return f"""
    <html>
    <head>
        <title>Ammo Catalog</title>
        <style>
            body {{ font-family: Arial; padding: 20px; }}
            .item {{ margin-bottom: 20px; }}
            img {{ width: 150px; }}
        </style>
        <script>
            function filterItems() {{
                var input = document.getElementById('search').value.toLowerCase();
                var items = document.querySelectorAll('.item');
                items.forEach(function(item) {{
                    var caliber = item.getAttribute('data-caliber').toLowerCase();
                    item.style.display = caliber.includes(input) ? 'block' : 'none';
                }});
            }}
        </script>
    </head>
    <body>
        <h1>Ammo Catalog</h1>
        <input type="text" id="search" onkeyup="filterItems()" placeholder="Search by caliber...">
        {items_html}
    </body>
    </html>
    """
