from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from orders.models import Order
from reviews.models import Review, ReviewImage, OwnerComment


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ('id', 'image')


class OwnerCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerComment
        fields = ('id', 'comments', 'created', 'review_id')


class ReviewListSerializer(serializers.ModelSerializer):
    images = ReviewImageSerializer(many=True, source='img', read_only=True)
    ownercomment = OwnerCommentSerializer()

    class Meta:
        model = Review
        fields = ('id', 'owner', 'order', 'restaurant', 'caption', 'like_count', 'rating', 'taste', 'amount',
                  'delivery', 'images', 'created', 'ownercomment')


class ReviewCreateSerializer(serializers.ModelSerializer):
    _img = ReviewImageSerializer(many=True, source='img', read_only=True)
    img = serializers.ListField(child=serializers.ImageField(), write_only=True, allow_null=True)

    class Meta:
        model = Review
        fields = ('id', 'taste', 'amount', 'delivery', 'restaurant', 'caption', 'menu_name', 'rating', 'owner', 'order',
                  'img', '_img',)
        read_only_fields = ('owner', 'order', 'rating', 'menu_name', 'restaurant')

    def validate(self, attrs):
        """request order_pk 가 리뷰 모델에 있는지 검증 """
        order_pk = self.context['view'].kwargs.get('order_pk')
        if order_pk is None:
            raise ValidationError('order_pk is missing')
        try:
            order = Order.objects.get(id=order_pk)
        except ObjectDoesNotExist:
            raise ValidationError('order_pk is wrong')
        is_duplicate = Review.objects.filter(order=order).exists()
        if is_duplicate:
            raise ValidationError('order can have only one review')
        return attrs

    def create(self, validated_data):
        """리뷰 저장할 때 이미지는 리뷰이미지 모델에 저장 """

        images = validated_data.pop('img')  # review 모델 안에 img 없음

        #  이미지 세장보다 많으면 error
        if 3 < len(images):
            raise ValidationError('image maximum 3!')

        review = Review.objects.create(**validated_data)
        image_list = [ReviewImage(review=review, image=image) for image in images]
        ReviewImage.objects.bulk_create(image_list)

        return review
