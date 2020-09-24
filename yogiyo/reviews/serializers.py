from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review, ReviewImage


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (  # todo 이미지필드
            'id', 'owner', 'order', 'restaurant', 'caption', 'like_count', 'rating', 'taste', 'amount', 'delivery')


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ('id', 'image',)


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
        order_pk = self.context['view'].kwargs['order_pk']
        is_order = Review.objects.filter(order_id=order_pk).first()
        if is_order is not None:
            raise ValidationError('this order already exists in Review models')

        return attrs

    def create(self, validated_data):
        """리뷰 저장할 때 이미지는 리뷰이미지 모델에 저장 """

        images = validated_data.pop('img')  # review 모델 안에 img 없음

        review = Review.objects.create(**validated_data)

        #  이미지 세장보다 많으면 error
        if 3 < len(images):
            raise ValidationError('image maximum 3! ')

        image_list = []
        for image in images:
            image_list.append(ReviewImage(review=review, image=image))

        ReviewImage.objects.bulk_create(image_list)

        return review
