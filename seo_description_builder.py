
def build_seo_description(title, caliber, rounds, price):
    base = f"{title} is a premium {caliber} round known for its consistency and reliability."

    usage = ""
    title_upper = title.upper()
    if "FMJ" in title_upper:
        usage = " Ideal for target shooting and training."
    elif "HP" in title_upper or "HOLLOW" in title_upper:
        usage = " Designed for maximum stopping power in self-defense scenarios."
    elif "SP" in title_upper or "SOFT" in title_upper:
        usage = " Great for hunting medium-sized game with controlled expansion."

    final = f"{base}{usage} Now available for ${price} per {rounds}-round box."

    return final
