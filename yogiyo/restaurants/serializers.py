from rest_framework import serializers
from taggit.models import Tag

from restaurants.models import Option, OptionGroup, Menu, MenuGroup, Restaurant


class DeliveryTimeField(serializers.Field):
    """delivery_time: 10 -> 10~20분"""

    def to_representation(self, value):
        return f'{value}~{value + 10}분'


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'name', 'price', 'option_group_id')
        examples = {
            'id': 1,
            'name': '호박 추가',
            'price': 1000,
            'option_group_id': 1
        }


class OptionGroupSerializer(serializers.ModelSerializer):
    option = OptionSerializer(read_only=True, many=True)

    class Meta:
        model = OptionGroup
        fields = ('id', 'name', 'menu_id', 'mandatory', 'option')
        examples = {
            'id': 1,
            'name': '채소 추가',
            'menu_id': 1,
            'mandatory': True
        }


class MenuDetailSerializer(serializers.ModelSerializer):
    option_group = OptionGroupSerializer(read_only=True, many=True)

    class Meta:
        model = Menu
        fields = ('id', 'name', 'image', 'caption', 'price', 'option_group')
        examples = {
            'id': 1,
            'name': '된장찌개',
            'caption': '보글보글 맛있는 된장찌개 입니다 ^^',
            'price': 6000,

        }


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
    delivery_time = DeliveryTimeField()
    bookmark_count = serializers.IntegerField(source='bookmark.count')

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'average_rating', 'image', 'back_image', 'delivery_discount', 'delivery_charge',
                  'delivery_time', 'review_count', 'representative_menus', 'owner_comment_count', 'bookmark_count',
                  'min_order_price')
        examples = {
            'id': '2',
            'name': '최고의 찌개',
            'average_rating': '3.9',
            'delivery_discount': '2000',
            'delivery_charge': '3000',
            'delivery_time': '30',
            'review_count': '10',
            'representative_menus': '김치찌개, 된장찌개, 부대찌개',
            'owner_comment_count': '7',
            'bookmark_count': '20',
            'min_order_price': '10000'
        }


class BookmarkRestaurantSerializer(RestaurantListSerializer):  # todo 지워버릴까?
    owner_comment_count = serializers.SerializerMethodField()

    class Meta(RestaurantListSerializer.Meta):
        pass

    def get_owner_comment_count(self, restaurant):
        # 사장님 댓글 수 - 0이면 null로
        return restaurant.owner_comment_count if restaurant.owner_comment_count != 0 else None

    def get_delivery_discount(self, restaurant):
        return restaurant.delivery_discount if restaurant.delivery_discount != 0 else None


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
