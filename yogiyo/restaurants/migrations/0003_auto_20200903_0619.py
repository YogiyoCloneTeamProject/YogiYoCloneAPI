# Generated by Django 3.1 on 2020-09-03 06:19

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_category_category_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='payment_method',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), size=None),
        ),
    ]
