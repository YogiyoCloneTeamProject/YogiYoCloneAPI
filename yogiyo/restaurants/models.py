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
    origin_information = models.CharField(max_length=255)