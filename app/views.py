from .forms import MealForm, MealFormSave, CreateUserForm
from .models import City, Restaurant, RestaurantAdress
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .utils import create_google_maps_link


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
    city_obj = City.objects.get(city_name=city_name)
    restaurants = Restaurant.objects.get(city_name_id=city_obj.id)
    return render(
        request,
        "restaurant.html",
        {"restaurants": restaurants, "city": city_obj.city_name},
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


