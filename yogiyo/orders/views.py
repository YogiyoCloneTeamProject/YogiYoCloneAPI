from rest_framework.viewsets import GenericViewSet

from orders.models import Order
from orders.serializers import OrderSerializer


class OrderViewSet(GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
