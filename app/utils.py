import logging
import requests
import re
from typing import Dict, Tuple, List

from django.db.models import QuerySet
from app.models import FoodType, Meal, ImgStorage

import pgeocode
from config import settings

COUNTY_CODE = "pl"


def sort_by_specified_order(
    food_types: QuerySet, order: Dict[str, int] = None
):
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
            logging.warning(
                f"Rank has not specified for {ft.food_type}. "
                f"It got one more that the biggest existed rank"
            )
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
                regex = re.compile("[^a-zA-Z]")
                result.append(regex.sub("", word).lower())
            else:
                result.append(word)
        return "_".join(result)

    temp_post = original_post.copy()
    temp_post["name"] = _modify_name(temp_post["name"])
    return temp_post


def menu_builder(
    menu: Dict[FoodType, Tuple[Tuple[Meal, ImgStorage]]]
) -> Dict[FoodType, List[Tuple[Meal, ImgStorage]]]:
    def modify_name(name):
        return name.replace("_", " ").title()

    result_menu = {}
    for ft, meal_tuples in menu.items():
        ft.food_type = modify_name(ft.food_type)
        meals = []
        for meal_img_tuple in meal_tuples:
            meal = meal_img_tuple[0]
            img = meal_img_tuple[1]
            meal.name = modify_name(meal.name)
            meals.append((meal, img))
        result_menu[ft] = meals
    return result_menu


def find_city_by_its_postal_code(postal_code: str):
    nomi = pgeocode.Nominatim(COUNTY_CODE)
    location_df = nomi.query_postal_code(postal_code)
    city = location_df["place_name"]
    return city


def get_coordinates(street: str, suite: str, city: str) -> Tuple[float, float]:
    address = f"{street}%20{suite},%20{city}"
    r = requests.get(
        "https://api.openrouteservice.org/geocode/search?api_key=%s&text=%s"
        % (
            settings.OPENROUTSERVICE_API_KEY,
            address,
        ),
    )
    request_json = r.json()
    return request_json["features"][0]["geometry"]["coordinates"]


def shortest_route_time(start: Tuple[float, float], end: Tuple[float, float]):
    start_lon, start_lat, end_lon, end_lat = start[0], start[1], end[0], end[1]
    r = requests.get(
        "https://api.openrouteservice.org/v2/directions/driving-car?api_key=%s&start=%s,%s&end=%s,%s"
        % (
            settings.OPENROUTSERVICE_API_KEY,
            start_lon,
            start_lat,
            end_lon,
            end_lat,
        )
    )
    request_json = r.json()
    duration = request_json["features"][0]["properties"]["summary"]["duration"]
    duration_in_min = duration / 60
    return duration_in_min
