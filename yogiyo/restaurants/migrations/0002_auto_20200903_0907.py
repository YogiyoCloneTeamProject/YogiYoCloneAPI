# Generated by Django 3.1 on 2020-09-03 09:07

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='caption',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='menugroup',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='option',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='optiongroup',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='business_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='categories',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), size=None),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='company_registration_number',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='delivery_time',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='opening_hours',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='payment_methods',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), size=None),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='tel_number',
            field=models.CharField(max_length=255),
        ),
    ]