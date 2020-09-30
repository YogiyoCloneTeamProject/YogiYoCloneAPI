from django.conf import settings
from django.db import models
from django.db.models import F

from orders.models import Order
from django.core.validators import MinValueValidator, MaxValueValidator

from restaurants.models import Restaurant


class Review(models.Model):
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='review')
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='review')
    caption = models.CharField(max_length=300)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    taste = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    delivery = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    amount = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='review')
    menu_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        """리뷰 생성할 때 해당 주문의 review_written -> true """
        self.order.review_written = True
        self.order.save()

        """리뷰 생성할 때 해당 레스토랑의 별점을 반영한다"""
        if not settings.CRAWLING:  # 크롤링 시 사용 X
            self.restaurant.average_taste = (
                                                        self.restaurant.average_taste * self.restaurant.review_count + self.taste) / (
                                                        self.restaurant.review_count + 1)
            self.restaurant.average_delivery = (
                                                           self.restaurant.average_delivery * self.restaurant.review_count + self.delivery) / (
                                                           self.restaurant.review_count + 1)
            self.restaurant.average_amount = (
                                                         self.restaurant.average_amount * self.restaurant.review_count + self.amount) / (
                                                         self.restaurant.review_count + 1)
            self.restaurant.average_rating = (
                                                         self.restaurant.average_taste + self.restaurant.average_delivery + self.restaurant.average_amount) / 3

        self.restaurant.review_count = F('review_count') + 1
        self.restaurant.save()


class ReviewImage(models.Model):
    """이미지 3장"""  # todo 리뷰 이미지 3장
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='img')
    image = models.ImageField(upload_to='review_image')


class ReviewComment(models.Model):
    review = models.OneToOneField('Review', on_delete=models.CASCADE)
    comments = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        """ restaurant - review_count +1 """
        print("g")
        print(Restaurant.objects.get(id=self.review.restaurant_id).review_count)
        Restaurant.objects.filter(id=self.review.restaurant_id).update(review_count=F('review_count') + 1)