from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from reviews.models import Review
from reviews.serializers import ReviewListSerializer


class ReviewViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    """review"""
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
