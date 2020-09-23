from rest_framework import serializers

from reviews.models import Review


# 다 이미지 추가해야함!!! 리스트로 ㅎㅎ

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'owner', 'order', 'caption', 'like_count', 'rating', 'taste', 'amount', 'delivery')


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'taste', 'amount', 'delivery', 'restaurant', 'caption', 'order_menu', 'rating', 'owner', 'order')
        read_only_fields = ('owner', 'order','rating')
