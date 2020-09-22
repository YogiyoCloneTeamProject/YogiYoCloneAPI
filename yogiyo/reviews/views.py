from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from reviews.models import Review
from reviews.serializers import ReviewListSerializer, ReviewCreateSerializer


class ReviewViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    """review"""
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer

    def get_serializer_class(self):
        if self.action == 'post': # todo 딜리트는 나중에..!
            return ReviewCreateSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


