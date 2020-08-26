from django.db import models


class Order(models.Model):
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)
    # status = models.TextChoices() todo order status choice field