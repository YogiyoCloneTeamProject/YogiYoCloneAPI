# Generated by Django 3.1 on 2020-09-28 05:37

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20200927_0749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_num',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]
