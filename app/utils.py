import logging
import re
from typing import Dict
from django.db.models import QuerySet

from app.models import FoodType


def sort_by_specified_order(food_types: QuerySet, order: Dict[str, int] = None):
    if not order:
        order = {
                    "pizza": 0,
                    "pasta": 1,
                    "soup": 2,
                    "salad": 3,
                    "dessert": 4,
                    "drink": 5,
                }

    def get_rank(ft: FoodType):
        try:
            rank = order[ft.food_type]
        except KeyError:
            logging.warning(f"Rank has not specified for {ft.food_type}. "
                            f"It got one more that the biggest existed rank")
            rank = max(order.values()) + 1
        return rank
    return sorted(food_types, key=get_rank)


def create_google_maps_link(adress):
    """Exp: https://maps.google.com/maps?q=Grodzka%2048,%2031-044%20Krak%C3%B3w&t=&z=15&ie=UTF8&iwloc=&output=embed"""
    city = adress.city.replace(" ", "+")
    street = adress.street.replace(" ", "+")

    return (
        f"https://maps.google.com/maps?q={street}%20{adress.building},"
        f"%20{adress.postal}%20{city}&t=&z=15&ie=UTF8&iwloc=&output=embed"
    )


def get_modified_post_data(original_post):
    def _modify_name(name):
        result = []
        for word in name.split():
            if not word.isalpha():
                regex = re.compile('[^a-zA-Z]')
                result.append(regex.sub("", word).lower())
            else:
                result.append(word)
        return "_".join(result)

    temp_post = original_post.copy()
    temp_post["name"] = _modify_name(temp_post["name"])
    return temp_post
