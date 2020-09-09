from collections import OrderedDict

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
        fields = ('id', 'name', 'menu_id', 'mandatory', 'option')


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
        fields = ('name', 'menu')


class RestaurantDetailSerializer(serializers.ModelSerializer):
    # todo 리뷰 보기
    menu_group = MenuGroupSerializer(read_only=True, many=True)

    def to_representation(self, instance):
        """레스토랑의 모든 메뉴 중 image가 있는 메뉴만 photo_menu에 추가"""
        # 모든 메뉴 가져오기
        menu_groups = instance.menu_group.all()
        res = []
        for menu_group in menu_groups:
            res += menu_group.menu.all()

        # is_photomenu가 트루면 추가
        res2 = []
        for menu in res:
            if menu.is_photomenu:
                res2.append(menu)

        # 모델 -> 딕셔너리
        menus = MenuListSerializer(read_only=True, many=True, instance=res2)
        photo_menu = OrderedDict({
            'name': 'photo_menu',
            'menu': menus.data
        })

        # menu_group에 photo_menu 필드에 추가
        a = super().to_representation(instance)
        a['menu_group'].insert(0, photo_menu)
        return a

    class Meta:
        model = Restaurant
        fields = (
            'id', 'name', 'star', 'image', 'notification', 'opening_hours', 'tel_number', 'address', 'min_order',
            'payment_methods', 'business_name', 'company_registration_number', 'origin_information',
            'delivery_discount', 'delivery_charge', 'delivery_time', 'back_image', 'lat', 'lng', 'menu_group')


class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        # todo 리뷰 개수, 사장님 댓글 수, 대표메뉴 , 배달시간
        model = Restaurant
        fields = ('id', 'name', 'star', 'image', 'delivery_discount', 'delivery_charge', 'categories')
