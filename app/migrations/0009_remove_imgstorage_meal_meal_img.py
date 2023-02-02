# Generated by Django 4.1.4 on 2023-01-18 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_imgstorage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imgstorage',
            name='meal',
        ),
        migrations.AddField(
            model_name='meal',
            name='img',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='app.imgstorage'),
        ),
    ]