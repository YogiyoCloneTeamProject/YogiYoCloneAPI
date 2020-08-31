from rest_framework import serializers

from orders.models import Order, OrderOption, OrderOptionGroup, OrderMenu


class OrderOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderOption
        fields = ('')


class OrderOptionGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderOptionGroup
        fields = ('')


class OrderMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMenu
        fields = ('')


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
