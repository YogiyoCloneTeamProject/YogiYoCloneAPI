from rest_framework import serializers

from reviews.models import Review


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'owner', 'caption', 'like_count', 'rating', 'taste', 'amount', 'delivery', 'created')
