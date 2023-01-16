from typing import Dict, List

from .forms import MealForm, MealFormSave, CreateUserForm
from .models import City, Restaurant, RestaurantAdress, FoodType, Meal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet

from .utils import create_google_maps_link, sort_by_specified_order, get_modified_post_data


def register_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account was created for {username}")
            return redirect("login")

    context = {"form": form}
    return render(request, "register.html", context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Username or password is incorrect")

    return render(request, "login.html", context={})


def logout_page(request):
    logout(request)
    return redirect("login")


def get_main(request):
    return render(request, "home_page/main.html")


@login_required(login_url="login")
def create_form(request, city_name, restaurant_name):
    error = None
    if request.method == "POST":
        request.POST = get_modified_post_data(request.POST)
        form = MealFormSave(request.POST)
        if form.is_valid():
            form.save()
            redirect(f"pizza/create/{city_name}")
    return render(
        request,
        "create.html",
        {
            "meal_form": MealForm(restaurant_name=restaurant_name),
            "error": error,
        },
    )


@login_required(login_url="login")
def get_all_city(request):
    cities = City.objects.all()
    return render(request, "cities.html", {"cities": cities})


# todo: refactor. In case if restaurants with the same city_obj.id will be more that 1, need to have a list of it.


def get_all_restaurants_for_specified_city(request, city_name):
    city_obj = City.objects.get(name=city_name)
    restaurants = Restaurant.objects.get(city_id=city_obj.id)
    return render(
        request,
        "restaurant.html",
        {"restaurants": restaurants, "city": city_obj.name},
    )


def order(request):
    cities_restaurants = {}
    cities = City.objects.all()
    for city_obj in cities:
        restaurant_obj = Restaurant.objects.get(city=city_obj.id)
        adress_obj = RestaurantAdress.objects.get(restaurant=restaurant_obj.id)
        google_link = create_google_maps_link(adress_obj)
        cities_restaurants[city_obj] = {restaurant_obj: {adress_obj.__str__(): google_link}}
        # cities_restaurants.setdefault(city_obj, []).append(restaurant_obj)

    return render(
        request,
        "order_page/order.html",
        context={
            "cities_restaurants": cities_restaurants,
        },
    )


def get_menu_for_given_restaurant(request, restaurant: str):
    restaurant_obj = Restaurant.objects.get(name=restaurant)
    food_types: QuerySet = FoodType.objects.filter(restaurant_id=restaurant_obj.id)
    sorted_food_types = sort_by_specified_order(food_types)
    menu = {}
    for ft in sorted_food_types:
        meals: QuerySet = Meal.objects.filter(food_type_id=ft.id)
        sorted_meal = sorted(meals, key=lambda meal: meal.name)
        menu[ft] = sorted_meal
    copied_menu = menu.copy()
    menu = to_handle(copied_menu)
    return render(
        request,
        "order_page/restaurant/order_restaurant.html",
        context={
            "restaurant_obj": restaurant_obj,
            "menu": menu,
        }
    )


def to_handle(menu: Dict[FoodType, List[Meal]]) -> Dict[FoodType, List[Meal]]:
    def modify_name(name):
        return name.replace("_", " ").title()

    result_menu = {}
    for ft, meal_list in menu.items():
        ft.food_type = modify_name(ft.food_type)
        meals = []
        for meal in meal_list:
            meal.name = modify_name(meal.name)
            meals.append(meal)
        result_menu[ft] = meals
    return result_menu
