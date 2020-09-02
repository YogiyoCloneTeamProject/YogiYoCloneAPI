from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    star = models.FloatField()
    notification = models.TextField()
    opening_hours = models.CharField(max_length=20)
    tel_number = models.CharField(max_length=40)
    address = models.CharField(max_length=50)
    min_order = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=50)
    business_name = models.CharField(max_length=20)
    company_registration_number = models.CharField(max_length=20)
    origin_information = models.TextField()
    image = models.ImageField(upload_to='restaurant_image', null=True, blank=True)
    delivery_discount = models.PositiveIntegerField(null=True, blank=True)
    delivery_charge = models.PositiveIntegerField(null=True, blank=True)


class MenuGroup(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='menu_group')
    name = models.CharField(max_length=40)


def menu_img_path(instance, filename):
    filename = filename.split('?')[0]
    print(filename)
    return f'menu_img/{filename}'


class Menu(models.Model):
    menu_group = models.ForeignKey('MenuGroup', on_delete=models.CASCADE, related_name='menu')
    name = models.CharField(max_length=40)
    image = models.ImageField(upload_to='menu_image', null=True, blank=True, max_length=400)
    caption = models.CharField(max_length=200)
    price = models.PositiveIntegerField()


class OptionGroup(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name='option_group')
    name = models.CharField(max_length=60)
    mandatory = models.BooleanField()


class Option(models.Model):
    option_group = models.ForeignKey('OptionGroup', on_delete=models.CASCADE, related_name='option')
    name = models.CharField(max_length=60)
    price = models.PositiveIntegerField()


class Category(models.Model):
    name = models.CharField(max_length=50)


class Category_Restaurant(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
