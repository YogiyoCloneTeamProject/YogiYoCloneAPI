from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from orders.models import Order
from orders.serializers import OrderSerializer


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
