# Generated by Django 4.1.4 on 2023-01-02 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_restaurantadress_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantadress',
            name='building',
            field=models.SlugField(default=None, max_length=4),
        ),
    ]
