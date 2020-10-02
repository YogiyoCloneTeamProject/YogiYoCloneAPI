from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from taggit.managers import TaggableManager


class CategoryChoice(models.TextChoices):
    ONE_SERVING = '1인분주문'
    FRANCHISE = '프랜차이즈'
    CHICKEN = '치킨'
    PIZZA = '피자양식'
    CHINESE = '중식'
    KOREAN = '한식'
    JAPANESE = '일식돈까스'
    JOKBAL = '족발보쌈'
    MIDNIGHT = '야식'
    SNACK = '분식'
    CAFE = '카페디저트'
    CONVENIENCE = '편의점'
    TAKEOUT = '테이크아웃'


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    average_rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    average_taste = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    average_delivery = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    average_amount = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    notification = models.TextField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    tel_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    min_order_price = models.PositiveIntegerField()
    payment_methods = ArrayField(models.CharField(max_length=255))
    business_name = models.CharField(max_length=255)
    company_registration_number = models.CharField(max_length=255)
    origin_information = models.TextField()
    image = models.ImageField(upload_to='restaurant_image', null=True, blank=True)
    delivery_discount = models.PositiveIntegerField(null=True, blank=True)  # 배달 할인
    delivery_charge = models.PositiveIntegerField(null=True, blank=True)  # 배달비
    delivery_time = models.PositiveIntegerField()  # 배달 예상 시간
    back_image = models.ImageField(upload_to='restaurant_back_image', null=True, blank=True)
    categories = ArrayField(models.CharField(max_length=20, choices=CategoryChoice.choices))
    lat = models.FloatField()
    lng = models.FloatField()
    review_count = models.PositiveIntegerField(default=0)
    representative_menus = models.CharField(max_length=255)
    tags = TaggableManager()
    owner_comment_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'({self.id}){self.name}'


class MenuGroup(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='menu_group')
    name = models.CharField(max_length=255)


def menu_img_path(instance, filename):
    filename = filename.split('?')[0]
    return f'menu_img/{filename}'


class Menu(models.Model):
    menu_group = models.ForeignKey('MenuGroup', on_delete=models.CASCADE, related_name='menu')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='menu_image', null=True, blank=True, max_length=400)
    caption = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    is_photomenu = models.BooleanField(default=False)


class OptionGroup(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name='option_group')
    name = models.CharField(max_length=255)
    mandatory = models.BooleanField(default=False)


class Option(models.Model):
    option_group = models.ForeignKey('OptionGroup', on_delete=models.CASCADE, related_name='option')
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
