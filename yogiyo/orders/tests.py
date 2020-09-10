from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase


class OrderCreateTestCase(APITestCase):
    """주문 생성"""

    def setUp(self) -> None:
        self.restaurant = baker.make('restaurants.Restaurant')
        menu_group = baker.make('restaurants.MenuGroup', restaurant=self.restaurant, name='햄버거')
        self.menu = baker.make('restaurants.Menu', menu_group=menu_group, name='띠드버거')
        option_groups = []
        option_groups += baker.make('restaurants.OptionGroup', _quantity=1, name='움료추가', mandatory=False,
                                    menu=self.menu)
        option_groups += baker.make('restaurants.OptionGroup', _quantity=1, name='패티추가', mandatory=True,
                                    menu=self.menu)
        # option = []
        # for i in range(len(option_groups)):
        #     option += baker.make('restaurants.Option', _quantity=1, option_group=option_groups[i], name=f'option{i}')

        options = baker.make('restaurants.Option', _quantity=2, option_group=option_groups[0])
        options2 = baker.make('restaurants.Option', _quantity=2, option_group=option_groups[1])

        self.url = f'/orders'
        self.data = {
            "restaurant": self.restaurant.id,
            "order_menu": [
                {
                    "menu": 1,
                    "name": self.menu.name,
                    "count": 1,
                    "price": self.menu.price,
                    "order_option_group": [
                        {
                            "name": option_groups[0].name,
                            "mandatory": False,
                            "order_option": [
                                {
                                    "name": options[0].name,
                                    "price": options[0].price
                                },
                                {
                                    "name": options[1].name,
                                    "price": options[1].price
                                }
                            ]
                        },
                        {
                            "name": option_groups[1].name,
                            "mandatory": True,
                            "order_option": [
                                {
                                    "name": options2[0].name,
                                    "price": options2[0].price
                                },
                                # {
                                #     "name": options2[1].name,
                                #     "price": options2[1].price
                                # }
                            ]
                        },
                    ]
                },
            ],
            "address": "중림동",
            "delivery_requests": "소스 많이 주세요",
            "payment_method": "현금결제"

        }
        self.data = {
            "restaurant": 2,
            "order_menu": [
                {
                    "menu": 107,
                    "name": "신메뉴",
                    "count": 1,
                    "price": 17900,
                    "order_option_group": [
                        {
                            "name": "사이즈 선택",
                            "mandatory": True,
                            "order_option": [
                                {
                                    "name": "솔로",
                                    "price": 0
                                }
                            ]
                        },
                        {
                            "name": "고기 선택",
                            "mandatory": True,
                            "order_option": [
                                {
                                    "name": "섞어（삼겹＋목살）",
                                    "price": 0
                                }
                            ]
                        }
                    ]
                }
            ],
            "address": "중림동",
            "delivery_requests": "소스 많이 주세요",
            "payment_method": "현금결제"
        }
        self.user = baker.make('users.User')

    def test_should_create(self):
        """생성-성공"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=self.data)
        res = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, res)
        print(res)
