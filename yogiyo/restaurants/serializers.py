from rest_framework import serializers

from restaurants.models import Option, OptionGroup, Menu, MenuGroup, Restaurant


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'name', 'price', 'option_group_id')


class OptionGroupSerializer(serializers.ModelSerializer):
    option = OptionSerializer(read_only=True, many=True)

    class Meta:
        model = OptionGroup
        fields = ('id', 'name', 'menu_id', 'option')


class MenuDetailSerializer(serializers.ModelSerializer):
    # todo 리뷰보기(개수) 추가
    option_group = OptionGroupSerializer(read_only=True, many=True)

    class Meta:
        model = Menu
        fields = ('id', 'name', 'image', 'caption', 'price', 'option_group')


class MenuListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'name', 'image', 'caption', 'menu_group_id', 'price')


class MenuGroupSerializer(serializers.ModelSerializer):
    menu = MenuListSerializer(read_only=True, many=True)

    class Meta:
        model = MenuGroup
        fields = ('id', 'name', 'restaurant_id', 'menu')


class RestaurantDetailSerializer(serializers.ModelSerializer):
    menu_list = MenuGroupSerializer(read_only=True, many=True)
    # todo 리뷰 보기

    class Meta:
        model = Restaurant
        fields = (
            'id', 'name', 'star', 'image', 'notification', 'opening_hours', 'tel_number', 'address', 'min_order',
            'payment_method', 'business_name', 'company_registration_number', 'origin_information', 'delivery_discount',
            'delivery_charge', 'menu_list')


class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        # todo 리뷰 개수, 사장님 댓글 수, 대표메뉴 , 배달시간
        model = Restaurant
        fields = ('id', 'name', 'star', 'image', 'delivery_discount', 'delivery_charge')
