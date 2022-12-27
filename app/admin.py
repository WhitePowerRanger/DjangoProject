from django.contrib import admin
from .models import City, Restaurant, Meal, FoodType


admin.site.register(City)
admin.site.register(Restaurant)
admin.site.register(Meal)
admin.site.register(FoodType)
