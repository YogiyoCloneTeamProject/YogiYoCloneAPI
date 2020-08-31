from rest_framework import serializers

from orders.models import Order, OrderOption, OrderOptionGroup, OrderMenu


class OrderOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderOption
        fields = ('id', 'name', 'price')


class OrderOptionGroupSerializer(serializers.ModelSerializer):
    order_option = OrderOptionSerializer(many=True)

    class Meta:
        model = OrderOptionGroup
        fields = ('id', 'name', 'order_option')


class OrderMenuSerializer(serializers.ModelSerializer):
    order_option_group = OrderOptionGroupSerializer(many=True)

    class Meta:
        model = OrderMenu
        fields = ('id', 'order_option_group', 'count')


class OrderSerializer(serializers.ModelSerializer):
    order_menu = OrderMenuSerializer(many=True)
    """주문 생성"""

    class Meta:
        model = Order
        fields = ('id', 'order_menu')


class OrderListSerializer(serializers.ModelSerializer):
    """주문 내역 리스트"""

    class Meta:
        model = Order
        fields = ('id',)
