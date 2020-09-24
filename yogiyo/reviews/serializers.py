from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review


# todo 이미지 필드 추가하기 !

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'owner', 'order', 'restaurant' ,'caption', 'like_count', 'rating', 'taste', 'amount', 'delivery')


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'taste', 'amount', 'delivery', 'restaurant', 'caption', 'menu_name', 'rating', 'owner', 'order')
        read_only_fields = ('owner', 'order', 'rating', 'menu_name', 'restaurant')

    def validate(self, attrs):
        """request order_pk 가 리뷰 모델에 있는지 검증 """
        order_pk = self.context['view'].kwargs['order_pk']
        is_order = Review.objects.filter(order_id=order_pk).first()
        if is_order is not None:
            raise ValidationError('this order already exists in Review models')

        return attrs
