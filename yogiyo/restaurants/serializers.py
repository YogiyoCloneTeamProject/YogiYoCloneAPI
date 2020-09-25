from rest_framework import serializers

from restaurants.models import Option, OptionGroup, Menu, MenuGroup, Restaurant


class DeliveryTimeField(serializers.Field):
    """delivery_time: 10 -> 10~20분"""

    def to_representation(self, value):
        return f'{value}~{value + 10}분'


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
    photo_menu = serializers.SerializerMethodField()
    delivery_time = DeliveryTimeField()

    def get_photo_menu(self, obj):
        m = MenuListSerializer(instance=Menu.objects.filter(menu_group__restaurant=obj, is_photomenu=True), many=True)
        return m.data

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'average_rating', 'average_taste', 'average_delivery', 'average_amount', 'image',
                  'back_image', 'notification', 'opening_time', 'closing_time', 'tel_number', 'address',
                  'min_order_price', 'payment_methods', 'business_name', 'company_registration_number',
                  'origin_information', 'delivery_discount', 'delivery_charge', 'delivery_time', 'photo_menu',
                  'menu_group', 'review_count')


class RestaurantListSerializer(serializers.ModelSerializer):
    representative_menus = serializers.SerializerMethodField()
    delivery_time = DeliveryTimeField()

    def get_representative_menus(self, obj):
        return '대표메뉴 추가 예정...'

    class Meta:
        # todo 사장님 댓글 수, 대표메뉴
        model = Restaurant
        fields = ('id', 'name', 'average_rating', 'image', 'delivery_discount', 'delivery_charge', 'delivery_time',
                  'review_count', 'representative_menus')


class HomeViewSerializer(serializers.ModelSerializer):
    delivery_time = DeliveryTimeField()
    bookmark_count = serializers.IntegerField(source='bookmark.count')

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'average_rating', 'image', 'delivery_discount', 'delivery_charge', 'delivery_time',
                  'bookmark_count', 'review_count', 'representative_menus', 'min_order_price')
