from django.db import models


class City(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default=None)
    adress = models.CharField(max_length=50, default=None)

    def __str__(self):
        return f"{self.name} - {self.adress}"


class FoodType(models.Model):
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    food_type = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.food_type


class Meal(models.Model):
    food_type = models.ForeignKey(FoodType, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default=None)
    price = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.food_type} - {self.name}"

