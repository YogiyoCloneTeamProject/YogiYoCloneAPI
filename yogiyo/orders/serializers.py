from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty

from orders.models import Order, OrderOption, OrderOptionGroup, OrderMenu
from restaurants.models import Menu
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
        fields = ('id', 'menu', 'name', 'count', 'order_option_group',)


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

    def validate(self, attrs):
        print(attrs)

        return super().validate(attrs)

    def create(self, validated_data):
        order_menus = validated_data.pop('order_menu')
        user = User.objects.first()
        order = Order.objects.create(owner=user, **validated_data)
        for order_menu in order_menus:
            order_option_groups = order_menu.pop('order_option_group')
            order_menu_obj = OrderMenu.objects.create(order=order, **order_menu)
            for order_option_group in order_option_groups:
                order_options = order_option_group.pop('order_option')
                order_option_group_obj = OrderOptionGroup.objects.create(order_menu=order_menu_obj,
                                                                         **order_option_group)
                for order_option in order_options:
                    OrderOption.objects.create(order_option_group=order_option_group_obj, **order_option)
        return order


class OrderListSerializer(serializers.ModelSerializer):
    """주문 내역 리스트"""

    class Meta:
        model = Order
        fields = ('id',)
