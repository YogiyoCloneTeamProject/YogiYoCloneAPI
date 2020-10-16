from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from core.permissions import IsOwnerAndIsAuthenticated
from orders.models import Order
from orders.serializers import OrderSerializer, OrderListSerializer, OrderCreateSerializer


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerAndIsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        주문 생성


        [req - model 데이터 일치 검증]
        order_menu -> 이름, 가격
        order_option_group -> 이름, mandatory, mandatory:true-> len(option_group) = 1,
        order_option -> 이름, 가격

        토큰 필요
        """
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        주문 조회


        유저가 주문한 주문 조회
        토큰 필요
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        주문 디테일 조회


        유저가 주문한 주문의 디테일 조회
        토큰 필요
        """
        return super().retrieve(request, *args, **kwargs)

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
        return qs.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
