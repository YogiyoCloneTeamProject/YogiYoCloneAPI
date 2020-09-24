from django.db import models

from orders.models import Order
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE)
    caption = models.CharField(max_length=300)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    taste = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    delivery = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    amount = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    order = models.OneToOneField(
        'orders.Order',
        on_delete=models.CASCADE
    )
    menu_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        self.order.review_written = True
        self.order.save()


class ReviewImage(models.Model):
    """이미지 3장"""  # todo 리뷰 이미지 3장
    review = models.ForeignKey('Review', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='review_image')


class ReviewComment(models.Model):
    review = models.OneToOneField('Review', on_delete=models.CASCADE)
    comments = models.CharField(max_length=300)
