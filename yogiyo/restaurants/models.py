from django.db import models
from django.contrib.postgres.fields import ArrayField


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    star = models.FloatField()
    notification = models.TextField()
    opening_hours = models.CharField(max_length=255)
    tel_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    min_order = models.PositiveIntegerField()
    payment_methods = ArrayField(models.CharField(max_length=255))
    business_name = models.CharField(max_length=255)
    company_registration_number = models.CharField(max_length=255)
    origin_information = models.TextField()
    image = models.ImageField(upload_to='restaurant_image', null=True, blank=True)
    delivery_discount = models.PositiveIntegerField(null=True, blank=True)
    delivery_charge = models.PositiveIntegerField(null=True, blank=True)
    delivery_time = models.CharField(max_length=255)
    back_image = models.ImageField(upload_to='restaurant_back_image', null=True, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()
    categories = ArrayField(models.CharField(max_length=255))


class MenuGroup(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='menu_group')
    name = models.CharField(max_length=255)


def menu_img_path(instance, filename):
    filename = filename.split('?')[0]
    print(filename)
    return f'menu_img/{filename}'


class Menu(models.Model):
    menu_group = models.ForeignKey('MenuGroup', on_delete=models.CASCADE, related_name='menu')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='menu_image', null=True, blank=True, max_length=400)
    caption = models.CharField(max_length=255)
    price = models.PositiveIntegerField()


class OptionGroup(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name='option_group')
    name = models.CharField(max_length=255)
    mandatory = models.BooleanField(default=False)


class Option(models.Model):
    option_group = models.ForeignKey('OptionGroup', on_delete=models.CASCADE, related_name='option')
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
