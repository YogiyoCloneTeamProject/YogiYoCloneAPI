from rest_framework import serializers
from rest_framework.fields import empty

from orders.models import Order, OrderOption, OrderOptionGroup, OrderMenu
from users.models import User


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
    """주문 조회"""
    order_menu = OrderMenuSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'order_menu')


class OrderCreateSerializer(serializers.ModelSerializer):
    """주문 생성"""
    order_menu = OrderMenuSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'order_menu', 'restaurant')

    def create(self, validated_data):
        order_menus = validated_data.pop('order_menu')
        user = User.objects.first()
        order = Order.objects.create(owner=user, **validated_data)
        for order_menu in order_menus:
            OrderMenu.objects.create(order=order, **order_menu)
        return order


class OrderListSerializer(serializers.ModelSerializer):
    """주문 내역 리스트"""

    class Meta:
        model = Order
        fields = ('id',)
