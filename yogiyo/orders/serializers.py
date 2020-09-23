from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from orders.models import Order, OrderOption, OrderOptionGroup, OrderMenu
from restaurants.models import Menu
from users.models import User


class OrderMenuNameField(serializers.Field):
    """order_menu: 치즈버거 x 1, 불고기버거 x 2"""

    def to_representation(self, value):
        names = [f'{order_menu.name} x {order_menu.count}' for order_menu in value.all()]
        return ', '.join(names)


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
        fields = ('id', 'menu', 'name', 'price', 'count', 'order_option_group')


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
        # todo 할인
        # 음식점 최소가격 확인
        if attrs['total_price'] < attrs['restaurant'].min_order_price:
            raise ValidationError('total price < restaurant min price')

        price_list = []
        # req - model 데이터 일치 확인
        order_menus = attrs['order_menu']
        for order_menu in order_menus:
            """req: 메뉴 이름, 가격 / model : 메뉴 이름, 가격 비교 """
            menu = order_menu['menu']
            # req 레스토랑이 메뉴 모델에 레스토랑과 같은지
            if order_menu['name'] != menu.name:
                raise ValidationError('menu.name != model menu.name')
            if order_menu['price'] != menu.price:
                raise ValidationError('menu.price != model menu.price')

            check_price = order_menu['price']

            """order_option_group"""
            for order_option_group in order_menu['order_option_group']:
                try:
                    is_order_option_group = menu.option_group.get(name=order_option_group['name'])
                except models.ObjectDoesNotExist:
                    raise ValidationError('This option group is not included in this menu')

                if order_option_group['mandatory'] != is_order_option_group.mandatory:
                    raise ValidationError('order_option_group.mandatory != model option_group.mandatory')
                # mandatory = true -> option 1개만!
                if order_option_group['mandatory']:
                    if len(order_option_group['order_option']) != 1:
                        raise ValidationError('mandatory true -> must len(order option list) == 1  ')

                """order_option"""
                for order_option in order_option_group['order_option']:
                    try:
                        is_order_option = is_order_option_group.option.get(name=order_option['name'])
                    except models.ObjectDoesNotExist:
                        raise ValidationError('This option is not included in this option group')

                    if order_option['price'] != is_order_option.price:
                        raise ValidationError('order option.price != model option.price')

                    check_price += order_option['price']

            check_price *= order_menu['count']
            price_list.append(check_price)

        # 총 가격 == (메뉴 가격 + 옵션 가격) * 주문 갯수
        if attrs['total_price'] != sum(price_list):
            raise ValidationError('total price != check_price')

        return attrs

    def create(self, validated_data):
        # todo create할 때 option_group option menu ordering
        order_menus = validated_data.pop('order_menu')
        user = User.objects.first()  # todo 테스트용 owner 빼기
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
    # todo status 주문 상태
    """주문 내역 리스트"""
    order_menu = OrderMenuNameField()
    status = serializers.SerializerMethodField()
    restaurant_name = serializers.CharField(source='restaurant.name')
    restaurant_image = serializers.ImageField(source='restaurant.image')

    class Meta:
        model = Order
        fields = ('id', 'order_menu', 'restaurant_name', 'restaurant_image', 'status', 'order_time')

    def get_status(self, obj):
        return '배달 상태 구현 예정...'
