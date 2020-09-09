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
        fields = ('id', 'name', 'order_option', 'mandatory')


class OrderMenuSerializer(serializers.ModelSerializer):
    order_option_group = OrderOptionGroupSerializer(many=True)

    class Meta:
        model = OrderMenu
        fields = ('id', 'menu', 'name', 'price', 'count', 'order_option_group',)


class OrderSerializer(serializers.ModelSerializer):
    """주문 조회"""
    order_menu = OrderMenuSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'order_menu', 'address', 'delivery_requests', 'payment_method')


class OrderCreateSerializer(serializers.ModelSerializer):
    """주문 생성"""
    order_menu = OrderMenuSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'order_menu', 'restaurant', 'address', 'delivery_requests', 'payment_method', 'total_price')

    def validate(self, attrs):
        """req 데이터와 model 데이터 검증 """
        order_menus = attrs['order_menu']
        for order_menu in order_menus:
            """req: 메뉴 이름, 가격 / model : 메뉴 이름, 가격 비교 """
            menu = Menu.objects.get(id=order_menu['menu'].id)
            if order_menu['name'] != menu.name:
                raise ValidationError('menu.name != model menu.name')
            if order_menu['price'] != menu.price:
                raise ValidationError('menu.price != model menu.price')

            """order_option_group"""
            for order_option_group in order_menu['order_option_group']:
                is_order_option_group = menu.option_group.get(name=order_option_group['name'])
                if not is_order_option_group:
                    raise ValidationError('order_option_group.name != model option_group.name')
                if order_option_group['mandatory'] != is_order_option_group.mandatory:
                    raise ValidationError('order_option_group.mandatory != model option_group.mandatory')

                """order_option"""
                for order_option in order_option_group['order_option']:
                    is_order_option = is_order_option_group.option.get(name=order_option['name'])
                    if not is_order_option:
                        raise ValidationError('order option.name != model option.name')
                    if order_option['price'] != is_order_option.price:
                        raise ValidationError('order option.price != model option.price')

        return super().validate(attrs)

    # def validate(self, attrs):
    #     """req 데이터와 model 데이터 검증 """
    #     order_menus = attrs['order_menu']
    #     for order_menu in order_menus:
    #         """req: 메뉴 이름, 가격 / model : 메뉴 이름, 가격 비교 """
    #         menu = Menu.objects.get(id=order_menu['menu'].id)
    #         if order_menu['name'] != menu.name:
    #             raise ValidationError('menu.name != model menu.name')
    #         if order_menu['price'] != menu.price:
    #             raise ValidationError('menu.price != model menu.price')
    #
    #         for order_option_group, order_option_group_obj in zip(order_menu['order_option_group'],
    #                                                               menu.option_group.all()):
    #             """req : 오더 옵션 그룹 이름, mandatory / model : 오더옵션그룹 이름, mandatory 비교 """
    #             if order_option_group['name'] != order_option_group_obj.name:
    #                 raise ValidationError('order_option_group.name != model option_group.name')
    #             if order_option_group['mandatory'] != order_option_group_obj.mandatory:
    #                 raise ValidationError('order_option_group.mandatory != model option_group.mandatory')
    #
    #             """mandatory true -> 옵션그룹에서 옵션이 한개만 왔는지 검증"""
    #             if order_option_group['mandatory'] and len(order_option_group['order_option']) != 1:
    #                 raise ValidationError('order_option_group is mandatory, but more then 1 option is given')
    #             for order_option, order_option_obj in zip(order_option_group['order_option'],
    #                                                       order_option_group_obj.option.all()):
    #                 if order_option['name'] != order_option_obj.name:
    #                     raise ValidationError('order option.name != model option.name')
    #                 if order_option['price'] != order_option_obj.price:
    #                     raise ValidationError('order option.price != model option.price')
    #
    #     """최소 주문 금액 검증 """  # todo 최소 주문 금액
    #
    #     return super().validate(attrs)

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
