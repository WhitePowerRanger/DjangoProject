

def create_google_maps_link(adress):
    """Exp: https://maps.google.com/maps?q=Grodzka%2048,%2031-044%20Krak%C3%B3w&t=&z=15&ie=UTF8&iwloc=&output=embed"""
    city = adress.city.replace(" ", "+")
    street = adress.street.replace(" ", "+")

    return (
        f"https://maps.google.com/maps?q={street}%20{adress.building},"
        f"%20{adress.postal}%20{city}&t=&z=15&ie=UTF8&iwloc=&output=embed"
    )
