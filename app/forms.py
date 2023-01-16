from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, CheckboxInput, Select, ModelChoiceField

from .models import Meal, City, Restaurant, FoodType
from django import forms


class MealForm(ModelForm):
    # todo: прокидывать (*args, **kwargs) вместо restaurant_name
    def __init__(self, **kwargs):
        restaurant_name = kwargs.pop("restaurant_name")
        restaurant = Restaurant.objects.get(name=restaurant_name)
        super(MealForm, self).__init__()
        self.fields["food_type"].queryset = FoodType.objects.filter(
            restaurant=restaurant.id
        )

    class Meta:
        model = Meal
        fields = "__all__"

    name = forms.TextInput()
    price = forms.IntegerField()
    availability = forms.BooleanField()
    food_type = ModelChoiceField(queryset=None, widget=forms.Select)


# todo: del MealFormSave. It should work with only one Form
class MealFormSave(ModelForm):
    class Meta:
        model = Meal
        fields = "__all__"
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Dish name",
                }
            ),
            "price": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Price",
                }
            ),
            "availability": CheckboxInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Availability",
                },
            ),
        }


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = "__all__"
        widgets = {
            "name": Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "City name",
                }
            )
        }


class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = "__all__"
        widgets = {
            "city_name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "City name",
                }
            ),
            "restaurant_name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Restaurant name",
                }
            ),
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Restaurant name",
                }
            ),
            "adress": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Adress",
                }
            ),
        }


class FoodTypeForm(ModelForm):
    class Meta:
        model = FoodType
        fields = "__all__"
        widgets = {
            "restaurant_name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Restaurant name",
                }
            ),
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
