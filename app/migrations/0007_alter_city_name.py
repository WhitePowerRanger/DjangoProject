# Generated by Django 4.1.4 on 2023-01-09 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_restaurant_adress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.SlugField(max_length=20, unique=True),
        ),
    ]
