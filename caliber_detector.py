
def detect_caliber_from_title(title):
    calibers = [
        "5.56x45mm NATO", "7.62x39mm", "223 Rem", ".223", "308 Win", ".308", "9mm", "10mm", "45 ACP",
        "12 Gauge", "20 Gauge", ".380", ".40 S&W", "300 AAC", "6.5 Creedmoor", "357 Magnum",
        "38 Special", "22 LR"
    ]
    title_lower = title.lower()
    matches = [cal for cal in calibers if cal.lower() in title_lower]
    return matches[0] if matches else "centerfire"
