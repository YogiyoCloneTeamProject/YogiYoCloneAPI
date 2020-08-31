from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """주문 생성"""
    class Meta:
        model = Order
        fields = ('')


class OrderListSerializer(serializers.ModelSerializer):
    """주문 내역 리스트"""
    class Meta:
        model = Order
        fields = ()
