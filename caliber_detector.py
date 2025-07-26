
def detect_caliber_from_title(title):
    import re
    calibers = [
        "9mm", "5.56", "223 Rem", ".223", "308 Win", ".308", "7.62", "12 Gauge", "10mm", "45 ACP",
        ".380", ".40 S&W", "300 AAC", "6.5 Creedmoor", "357 Magnum", "38 Special", "22 LR"
    ]
    for cal in calibers:
        if cal.lower() in title.lower():
            return cal
    return "centerfire"
