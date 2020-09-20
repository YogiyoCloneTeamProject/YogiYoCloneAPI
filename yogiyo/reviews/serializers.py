from rest_framework import serializers

from reviews.models import Review


class ReviewListSerializer(serializers.ModelSerializer):
    model = Review
    # 레스토랑이랑 오더 추가
    fields = ('owner', 'caption', 'rating', 'taste', 'amount', 'delivery', 'created')
