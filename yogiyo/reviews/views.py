from django.shortcuts import render
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet

from orders.models import Order
from reviews.models import Review
from reviews.serializers import ReviewListSerializer, ReviewCreateSerializer


class ReviewViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    """review"""
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer

    def get_serializer_class(self):
        if self.action == 'create':  # todo 딜리트는 나중에..!
            return ReviewCreateSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        if 'order_pk' in self.kwargs:
            order = get_object_or_404(Order, id=self.kwargs.get('order_pk'))
            rating = int((self.request.data['taste']+self.request.data['delivery'] + self.request.data['amount'])/3)

            serializer.save(
                owner=self.request.user,
                order=order,
                rating=rating,
                restaurant=order.restaurant,
                order_menu=order.order_menu  # string  으로...
            )

    # def get_queryset(self):
        # queryset = super().get_queryset().filter(=self.kwargs.get('order_pk'))
        # return queryset
