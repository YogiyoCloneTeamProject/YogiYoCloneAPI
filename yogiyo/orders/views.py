from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from orders.models import Order
from orders.serializers import OrderSerializer, OrderListSerializer, OrderCreateSerializer


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        if self.action == 'retrieve':
            return OrderSerializer
        if self.action == 'list':
            return OrderListSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
