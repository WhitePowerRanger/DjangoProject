# Generated by Django 4.1.4 on 2022-12-27 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FoodType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_type', models.CharField(default=None, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=50)),
                ('adress', models.CharField(default=None, max_length=50)),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.city')),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=50)),
                ('price', models.PositiveIntegerField(default=0)),
                ('available', models.BooleanField(default=False)),
                ('food_type', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.foodtype')),
            ],
        ),
        migrations.AddField(
            model_name='foodtype',
            name='restaurant_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.restaurant'),
        ),
    ]