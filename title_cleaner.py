
import re

def clean_title(title):
    return re.sub(r'[\s\-–]*(\d{2,4})[ -]?ct$', '', title, flags=re.IGNORECASE).strip()
