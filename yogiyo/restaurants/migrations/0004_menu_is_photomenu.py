# Generated by Django 3.1 on 2020-09-09 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_auto_20200904_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='is_photomenu',
            field=models.BooleanField(default=False),
        ),
    ]