from django.db import models


class Order(models.Model):
    class PaymentMethodChoice(models.TextChoices):
        CASH = 'CASH', '현금'
        CREDIT_CARD = 'CREDIT_CARD', '신용카드'
        YOGIYO_PAY = 'YOGIYO_PAY', '요기서결제'

    class OrderStatusChoice(models.TextChoices):
        WAITING_FOR_RECEIPT = 'WAITING_FOR_RECEIPT', '접수 대기 중'
        RECEIPT_COMPLETE = 'RECEIPT_COMPLETE', '접수 완료'
        DELIVERY = 'DELIVERY', '배달 중'
        DELIVERY_COMPLETE = 'DELIVERY_COMPLETE', '배달 완료'

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='order')
    order_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=OrderStatusChoice.choices,
                              default=OrderStatusChoice.WAITING_FOR_RECEIPT)
    address = models.CharField(max_length=255)
    delivery_requests = models.CharField(max_length=255, default="(없음)")
    payment_method = models.CharField(max_length=20, choices=PaymentMethodChoice.choices)
    total_price = models.PositiveIntegerField()
    review_written = models.BooleanField(default=False)


class OrderMenu(models.Model):
    menu = models.ForeignKey('restaurants.Menu', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_menu')
    name = models.CharField(max_length=255)
    count = models.PositiveIntegerField()
    price = models.PositiveIntegerField()


class OrderOptionGroup(models.Model):
    order_menu = models.ForeignKey('OrderMenu', on_delete=models.CASCADE, related_name='order_option_group')
    name = models.CharField(max_length=255)
    mandatory = models.BooleanField(default=False)


class OrderOption(models.Model):
    order_option_group = models.ForeignKey('OrderOptionGroup', on_delete=models.CASCADE, related_name='order_option')
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
