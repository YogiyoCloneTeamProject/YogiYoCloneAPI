from django.db import models


class Order(models.Model):
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='order')
    order_time = models.DateTimeField(auto_now_add=True)
    # status = models.TextChoices() todo order status choice field


class OrderMenu(models.Model):
    menu = models.ForeignKey('restaurants.Menu', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_menu')
    name = models.CharField(max_length=255)
    count = models.PositiveIntegerField()


class OrderOptionGroup(models.Model):
    order_menu = models.ForeignKey('OrderMenu', on_delete=models.CASCADE, related_name='order_option_group')
    name = models.CharField(max_length=255)
    # mandatory = models.BooleanField()  # todo mandatory = 필수 or 선택


class OrderOption(models.Model):
    order_option_group = models.ForeignKey('OrderOptionGroup', on_delete=models.CASCADE, related_name='order_option')
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
