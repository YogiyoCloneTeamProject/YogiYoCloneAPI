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
        fields = ('owner', 'order', ' caption', 'taste', 'amount', 'delivery')
