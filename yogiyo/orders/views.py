from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from core.permissions import IsOwner
from orders.models import Order
from orders.serializers import OrderSerializer, OrderListSerializer, OrderCreateSerializer


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]  # todo 퍼미션 추가
    # permission_classes = [IsOwner]


    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        if self.action == 'retrieve':
            return OrderSerializer
        if self.action == 'list':
            return OrderListSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list':
            if self.request.user.is_authenticated:
                # 로그인
                qs = qs.filter(owner=self.request.user)
            else:
                # todo 비로그인 삭제
                qs = Order.objects.all()
        return qs
