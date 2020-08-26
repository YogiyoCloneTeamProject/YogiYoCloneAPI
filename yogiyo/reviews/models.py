from django.db import models


class Review(models.Model):
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE)
    caption = models.CharField(max_length=300)
    rating = models.PositiveIntegerField()
    taste = models.PositiveIntegerField()
    delivery = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']


class ReviewImage(models.Model):
    """이미지 3장"""
    review = models.ForeignKey('Review', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='review_image')


class ReviewComment(models.Model):
    review = models.OneToOneField('Review', on_delete=models.CASCADE)
    comments = models.CharField(max_length=300)
