from rest_framework import serializers
from taggit.models import Tag

from orders.models import Order
from restaurants.models import Option, OptionGroup, Menu, MenuGroup, Restaurant


def extra_time(delivery_time, restaurant_id):
    """
    order에 레스토랑의 RECEIPT_COMPLETE인 상태 x (기본 조리 시간/2)
    """
    receipt_complete_count = Order.objects.filter(restaurant_id=restaurant_id, status='접수 완료').count() // 3
    delivery_time += receipt_complete_count * (delivery_time // 2)
    return f'{delivery_time}~{delivery_time + 10}분'


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'name', 'price', 'option_group_id')
        examples = {
            "id": 5442,
            "name": "뿌링뿌링소스 추가",
            "price": 1500,
            "option_group_id": 820
        }


class OptionGroupSerializer(serializers.ModelSerializer):
    option = OptionSerializer(read_only=True, many=True)

    class Meta:
        model = OptionGroup
        fields = ('id', 'name', 'menu_id', 'mandatory', 'option')
        examples = {
            "id": 820,
            "name": "변경&추가",
            "menu_id": 618,
            "mandatory": False,
        }


class MenuDetailSerializer(serializers.ModelSerializer):
    option_group = OptionGroupSerializer(read_only=True, many=True)

    class Meta:
        model = Menu
        fields = ('id', 'name', 'image', 'caption', 'price', 'option_group')
        examples = {
            "id": 618,
            "name": "뿌링맵소킹",
            "image": "https://yogiyo-s3.s3.ap-northeast-2.amazonaws.com/media/menu_image/ECA09CED9CB4FR_20200914_BHC_EBBF8CEBA781EBA7B5EC868CED82B9_1080x640_5zw8kTT.jpg",
            "caption": "뿌맵뿌맵! 혀를 찌르는 청양고추 시즈닝을 더해 세상에 없던 화려한 매운 맛",
            "price": 17000
        }


class MenuListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'name', 'image', 'caption', 'menu_group_id', 'price')
        examples = {
            "id": 618,
            "name": "뿌링맵소킹",
            "image": "https://yogiyo-s3.s3.ap-northeast-2.amazonaws.com/media/menu_image/ECA09CED9CB4FR_20200914_BHC_EBBF8CEBA781EBA7B5EC868CED82B9_1080x640_flBp3R5.jpg",
            "caption": "뿌맵뿌맵! 혀를 찌르는 청양고추 시즈닝을 더해 세상에 없던 화려한 매운 맛",
            "menu_group_id": 81,
            "price": 17000
        }


class MenuGroupSerializer(serializers.ModelSerializer):
    menu = MenuListSerializer(read_only=True, many=True)

    class Meta:
        model = MenuGroup
        fields = ('name', 'menu')
        examples = {
            "name": "신메뉴",
        }


class RestaurantDetailSerializer(serializers.ModelSerializer):
    menu_group = MenuGroupSerializer(read_only=True, many=True)
    photo_menu = serializers.SerializerMethodField()
    delivery_time = serializers.SerializerMethodField()

    def get_delivery_time(self, obj):
        return extra_time(obj.delivery_time, obj.id)

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
        examples = {
            "id": 10,
            "name": "BHC-성수점",
            "average_rating": 4.6,
            "average_taste": 4.6,
            "average_delivery": 4.6,
            "average_amount": 4.7,
            "image": "https://yogiyo-s3.s3.ap-northeast-2.amazonaws.com/media/restaurant_image/BHC_20191014_Franchise_crop_200x200_hY0tGRI_zwpjlBg.jpg",
            "back_image": "https://yogiyo-s3.s3.ap-northeast-2.amazonaws.com/media/restaurant_back_image/20191014171511754363_c7be81a92573dbcea9bc5988012d0051_tn_yoGfukV.jpg",
            "notification": "",
            "opening_time": "11:00:00",
            "closing_time": "00:30:00",
            "tel_number": "050352576406",
            "address": "서울 성동구 성수동1가 13-162 1층",
            "min_order_price": 15000,
            "payment_methods": [
                "신용카드",
                "현금",
                "요기서결제"
            ],
            "business_name": "BHCBeerZone(비에이치씨비어존)",
            "company_registration_number": "204-22-99067",
            "origin_information": "*닭고기 : 국내산  \r\n*소시지(돼지고기) : 국내산",
            "delivery_discount": 2000,
            "delivery_charge": 2000,
            "delivery_time": "45~55분",
            "photo_menu": [
                {
                    "id": 619,
                    "name": "뿌링맵소킹 콤보",
                    "image": "https://yogiyo-s3.s3.ap-northeast-2.amazonaws.com/media/menu_image/ECA09CED9CB4FR_20200730_BHC_EBBF8CEBA781EBA7B5EC868CED82B9ECBDA4EBB3B4_1080x640_L71SV2q.jpg",
                    "caption": "뿌맵뿌맵! 혀를 찌르는 청양고추 시즈닝을 더해 세상에 없던 화려한 매운 맛, 퍽퍽한 닭가슴살 없이 윙과 닭다리만 담은 콤보",
                    "menu_group_id": 81,
                    "price": 18000
                },
                {
                    "id": 624,
                    "name": "양념맵소킹 콤보",
                    "image": "https://yogiyo-s3.s3.ap-northeast-2.amazonaws.com/media/menu_image/ECA09CED9CB4FR_20200730_BHC_EC9691EB8590EBA7B5EC868CED82B9ECBDA4EBB3B4_1080x640_PxDegFe.jpg",
                    "caption": "맵소맵소! \"맵소킹\" 감탄과 함께 눈물이 찔끔 날 듯한 홍고추의 알싸한 매운 맛, 퍽퍽한 닭가슴살 없이 윙과 닭다리만 담은 콤보",
                    "menu_group_id": 81,
                    "price": 18000
                }],
            "review_count": 5
        }


class RestaurantListSerializer(serializers.ModelSerializer):
    delivery_time = serializers.SerializerMethodField()
    bookmark_count = serializers.IntegerField(source='bookmark.count')

    def get_delivery_time(self, obj):
        return extra_time(obj.delivery_time, obj.id)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'average_rating', 'image', 'back_image', 'delivery_discount', 'delivery_charge',
                  'delivery_time', 'review_count', 'representative_menus', 'owner_comment_count', 'bookmark_count',
                  'min_order_price')
        examples = {
            "id": 10,
            "name": "BHC-성수점",
            "average_rating": 4.6,
            "image": "https://yogiyo-s3.s3.ap-northeast-2.amazonaws.com/media/restaurant_image/BHC_20191014_Franchise_crop_200x200_hY0tGRI_zwpjlBg.jpg",
            "back_image": "https://yogiyo-s3.s3.ap-northeast-2.amazonaws.com/media/restaurant_back_image/20191014171511754363_c7be81a92573dbcea9bc5988012d0051_tn_yoGfukV.jpg",
            "delivery_discount": 2000,
            "delivery_charge": 2000,
            "delivery_time": "45~55분",
            "review_count": 5,
            "representative_menus": "뿌링클, 뿌링클순살",
            "owner_comment_count": 100,
            "bookmark_count": 0,
            "min_order_price": 15000
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
        examples = {
            'id': 1,
            'name': '떡볶이'
        }
